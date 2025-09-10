from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.schemas.user_schema import UserRequest, UserUpdateRequest

class UserRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_users(self, limit: int, offset: int):
        query = text("SELECT * FROM users ORDER BY id LIMIT :limit OFFSET :offset;")
        result = await self.db.execute(query, {"limit": limit, "offset": offset})
        return result.mappings().all()



    async def get_user_by_id(self, user_id: int):
        query = text("SELECT * FROM users WHERE id = :id")
        result = await self.db.execute(query, {"id": user_id})
        return result.mappings().first() # None if not found
    

    async def get_user_by_email(self, user_email: str):
        result = await self.db.execute(text("SELECT * FROM users WHERE email = :email"), {"email": user_email})
        return result.mappings().first()
    

    async def get_user_by_username(self, user_username: str):
        result = await self.db.execute(text("SELECT * FROM users WHERE username = :username"), {"username": user_username})
        return result.mappings().first()


    async def create_user(self, user_data: UserRequest):
        query = text(
            """
            INSERT INTO users (first_name, last_name, username, email, hashed_password)
            VALUES (:first_name, :last_name, :username, :email, :hashed_password)
            RETURNING *;
            """
        )

        result = await self.db.execute(query, user_data)
        await self.db.commit()
        return result.mappings().first()



    async def update_user(self, user_id: int, user_data: UserUpdateRequest):
        
        set_clause = ", ".join([f"{key} = :{key}" for key in user_data.keys()])
        query = text(f"UPDATE users SET {set_clause} WHERE id = :id")
        data = {**user_data, "id": user_id}

        await self.db.execute(query, data)
        await self.db.commit()
        return 
    

    async def increment_token_version(self, user_id: int):
        query = text("UPDATE users SET token_version = token_version + 1 WHERE id = :user_id")
        await self.db.execute(query, {"user_id": user_id})
        await self.db.commit()
 

