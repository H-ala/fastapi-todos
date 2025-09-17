import pytest
import pytest_asyncio
from app.main import app
from app.core.database import get_db
from app.core.config import settings
from alembic import command
from alembic.config import Config
import os
from httpx import ASGITransport, AsyncClient
from app.utils.security import create_access_token

# تنظیمات دیتابیس تست
DATABASE_URL = f"{settings.DATABASE_URL}_test"
ALEMBIC_DATABASE_URL = DATABASE_URL.replace("asyncpg", "psycopg2")

@pytest.fixture
def setup_test_database():
    """تنظیم اولیه دیتابیس"""
    os.environ['TEST_DATABASE_URL'] = ALEMBIC_DATABASE_URL
    try:
        alembic_cfg = Config(os.path.join(os.path.dirname(__file__), "../alembic.ini"))
        command.downgrade(alembic_cfg, "base")
        command.upgrade(alembic_cfg, "head")
        yield
    finally:
        command.downgrade(alembic_cfg, "base")
        os.environ.pop('TEST_DATABASE_URL', None)

@pytest_asyncio.fixture
async def session_context(setup_test_database):
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    from sqlalchemy.orm import sessionmaker

    test_engine = create_async_engine(DATABASE_URL, echo=True)
    TestingSessionLocal = sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    class AsyncSessionContext:
        def __init__(self):
            self.session = None
        async def get_session(self):
            if self.session is None:
                self.session = TestingSessionLocal()
            return self.session
        async def close_session(self):
            if self.session:
                await self.session.close()
                self.session = None

    context = AsyncSessionContext()
    yield context
    await context.close_session()
    await test_engine.dispose()

@pytest_asyncio.fixture
async def client(session_context):
    async def override_get_db():
        session = await session_context.get_session()
        try:
            yield session
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
    app.dependency_overrides.clear()

@pytest_asyncio.fixture
async def test_user(client):
    user_data = {
        "first_name": "Hosein",
        "last_name": "Ala",
        "username": "hala",
        "email": "hos.ala81@gmail.com", 
        "password": "123", 
        "repeat_password": "123" 
    }
    res = await client.post("/api/v1/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    user_data = {
        "id": 1,
        "email": test_user["email"],
        "role": "user",
        "token_version": 0
    }
    return create_access_token(user_data)


@pytest_asyncio.fixture
async def authorized_client(client, token):
    headers = {**client.headers, "Authorization": f"Bearer {token}"}
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
        headers=headers
    ) as ac:
        yield ac




@pytest_asyncio.fixture
async def test_todos(test_user, authorized_client):
    todos_data = [
        { 
            "title": "Learning React",
            "description": "it is gonna be long!!!!",
            "priority": 4,
            "complete": False
        },
        { 
            "title": "Learning FastAPI",
            "description": "it is gonna be tedious!",
            "priority": 5,
            "complete": False
        },
        {
            "title": "Enjoying Tabriz",
            "description": "it is gonna be fun!",
            "priority": 5,
            "complete": True
        },
        { 
            "title": "Stop sth",
            "description": "it is gonna be hard",
            "priority": 5,
            "complete": False
        }
    ]

    created_todos = []

    for todo in todos_data:
        res = await authorized_client.post("/api/v1/todos/", json=todo)
        assert res.status_code == 201
        created_todos.append(res.json())

    return created_todos















