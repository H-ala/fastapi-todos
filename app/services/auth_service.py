from app.repos.auth_repo import AuthRepo
from app.repos.user_repo import UserRepo
from app.utils.security import decode_access_token
from app.errors.auth_errors import InvalidCredentials, RevokedToken, FieldRequired, InvalidToken
from app.errors.user_errors import UserNotFound
from jose import JWTError
from app.utils.security import verify_password, hash_refresh_token, create_access_token
from app.core.config import settings
from datetime import datetime, timedelta




class AuthService:
    def __init__(self, auth_repo: AuthRepo, user_repo: UserRepo):
        self.auth_repo = auth_repo
        self.user_repo = user_repo


    async def authenticate_user(self, username: str, email: str, password: str):
        if not username and not email:
            raise FieldRequired()
        if username:
            user = await self.user_repo.get_user_by_username(username)

        elif email:
            user = await self.user_repo.get_user_by_email(email)

        if not user:
            raise UserNotFound()
        if not verify_password(password, user.hashed_password):
            raise InvalidCredentials()
            
        return user
    
            

    async def get_current_user(self, token: str):
        try: 
            payload = decode_access_token(token)
            user_id = int(payload.get("sub"))
            token_version = payload.get("token_version", 0)
            if not user_id:
                raise InvalidToken()
        except JWTError as e:
            raise InvalidToken()
        
        user = await self.user_repo.get_user_by_id(user_id)
        if not user:
            UserNotFound()
        if token_version != user["token_version"]:
            raise RevokedToken()
        return user
    



    async def save_refresh_token(self, refresh_token: str, user_id: int):

        user_last_refresh_token = await self.auth_repo.find_the_last_refresh_token(user_id)
        if user_last_refresh_token:
            await self.auth_repo.revoke_token(user_id)
        now = datetime.now()
        refresh_token_data = {}
        refresh_token_data["user_id"] = user_id
        refresh_token_data["jti"] = hash_refresh_token(refresh_token)
        refresh_token_data["expires_at"] = now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        # retrieve user's previous refresh token
        refresh_token_data["replaced_by"] = user_last_refresh_token.jti if user_last_refresh_token else None
        return await self.auth_repo.save_refresh_token(refresh_token_data)
    

    async def verify_refresh_token(self, refresh_token_req: str):
        hashed_refresh_token = hash_refresh_token(refresh_token_req)
        refresh_token_verified = await self.auth_repo.find_refresh_token(hashed_refresh_token)
        if not refresh_token_verified or refresh_token_verified["revoked"]:
            raise InvalidToken()
        
        user_data = await self.user_repo.get_user_by_id(refresh_token_verified["user_id"])
        
        return create_access_token(user_data)
    

    async def log_out(self, user_id:int):
        await self.user_repo.increment_token_version(user_id)
        await self.auth_repo.revoke_token(user_id)
        
        



