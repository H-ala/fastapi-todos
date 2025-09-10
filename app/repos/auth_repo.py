from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.schemas.auth_schema import RefreshToken

class AuthRepo:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def find_refresh_token(self, hashed_jti: str):
        query = text("SELECT * FROM refresh_token WHERE jti = :jti;")
        result = await self.db.execute(query, {"jti": hashed_jti})
        return result.mappings().first()



    async def save_refresh_token(self, refresh_token_data: RefreshToken):
        query = text(
            """
            INSERT INTO refresh_token(user_id, jti, expires_at, replaced_by)
            VALUES (:user_id, :jti, :expires_at, :replaced_by)
            RETURNING *;
            """
        )
        try:
            result = await self.db.execute(query, refresh_token_data)
            await self.db.commit()
            return result.mappings().first()
        except Exception as e:
            print("DB ERROR:", e)
            await self.db.rollback()
            raise


    async def find_the_last_refresh_token(self, user_id: int):
        result = await self.db.execute(text("SELECT * FROM refresh_token WHERE user_id = :user_id ORDER BY created_at DESC;"), {"user_id": user_id})
        return result.mappings().first()

    async def revoke_token(self, user_id: int):
        await self.db.execute(text("UPDATE refresh_token SET revoked = TRUE WHERE user_id = :user_id"), {"user_id": user_id})
        await self.db.commit()
