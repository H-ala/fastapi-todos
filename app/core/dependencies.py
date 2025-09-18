from app.services.auth_service import AuthService
from app.repos.auth_repo import AuthRepo
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from fastapi import Depends
from app.repos.user_repo import UserRepo
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from fastapi.security import OAuth2PasswordBearer
from typing import List
from app.errors.auth_errors import InsufficientPermission
from app.repos.todo_repo import TodoRepo
from app.services.todo_service import TodoService






oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_todo_repo(db: AsyncSession = Depends(get_db)) -> TodoRepo:
    return TodoRepo(db)

def get_user_repo(db: AsyncSession = Depends(get_db)) -> UserRepo:
    return UserRepo(db)

def get_auth_repo(db: AsyncSession = Depends(get_db)) -> AuthRepo:
    return AuthRepo(db)

def get_todo_service(repo: TodoRepo = Depends(get_todo_repo)) -> TodoService:
    return TodoService(repo)

def get_user_service(repo: UserRepo = Depends(get_user_repo)) -> UserService:
    return UserService(repo)

def get_auth_service(auth_repo: AuthRepo = Depends(get_auth_repo), user_repo: UserRepo = Depends(get_user_repo)) -> AuthService:
    return AuthService(auth_repo, user_repo)

async def get_current_user(token: str = Depends(oauth2_scheme), auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.get_current_user(token)

def role_checker(allowed_roles: List[str]):
    def dependency(current_user=Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise InsufficientPermission
        return current_user
    return dependency


