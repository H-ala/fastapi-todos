from app.repos.user_repo import UserRepo
from app.utils.security import hash_password, verify_password
from datetime import datetime
from app.errors.user_errors import (
    UserNotFound, EmailAlreadyExists, UsernameAlreadyExists,
    PasswordMismatch, PasswordAlreadySet, NothingToUpdate
)
from app.errors.auth_errors import InsufficientPermission 




class UserValidator:
    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo 


    async def validate_email(self, email: str):
        if await self.user_repo.get_user_by_email(email):
            raise EmailAlreadyExists(f"Email '{email}' already exists")
        
    async def validate_username(self, username: str):
        if await self.user_repo.get_user_by_username(username):
            raise UsernameAlreadyExists(f"Username '{username}' already exists")
    @staticmethod
    def validate_user(user):
        if user is None:
            raise UserNotFound(f"User not found")
        
    @staticmethod
    def validate_role(current_user, user_id):
        if not current_user.id == user_id and current_user.role == 'user':
            raise InsufficientPermission()
        
    @staticmethod
    def validate_password(password, repeat_password):
        if password != repeat_password:
            raise PasswordMismatch("Passwords are not identical")
        




class UserService:
    def __init__(self, user_repo: UserRepo, 
                 validator: UserValidator = None):
        self.user_repo = user_repo
        self.validator = validator or UserValidator(user_repo)


    async def get_user_by_id(self, current_user, user_id):
        user = await self.user_repo.get_user_by_id(user_id)
        self.validator.validate_user(user)
        self.validator.validate_role(current_user, user_id)
        return user    


    async def create_user(self, user_data):
        await self.validator.validate_email(user_data["email"])
        await self.validator.validate_username(user_data["username"])
        self.validator.validate_password(user_data["password"], user_data["repeat_password"])
        
        user_data.pop("repeat_password")
        user_data["hashed_password"] = hash_password(user_data.pop("password"))

        return await self.user_repo.create_user(user_data)


    async def update_user(self, current_user, user_id, user_data):
        user = await self.user_repo.get_user_by_id(user_id)

        self.validator.validate_user(user)
        self.validator.validate_role(current_user, user_id)
        fields_to_update = {k: v for k, v in user_data.items() if v is not None}

        if not fields_to_update:
            raise NothingToUpdate("No fields provided for update")

        if "email" in fields_to_update:
            await self.validator.validate_email(fields_to_update["email"])

        if "username" in fields_to_update:
            await self.validator.validate_username(fields_to_update["username"])
        
        if "password" in fields_to_update:
            self.validator.validate_password(fields_to_update["password"], fields_to_update.get("repeat_password", ""))
            if verify_password(fields_to_update["password"], user.hashed_password):
                raise PasswordAlreadySet("This password is already set")
            fields_to_update.pop("repeat_password", None)
            fields_to_update["hashed_password"] = hash_password(fields_to_update.pop("password"))


        fields_to_update["updated_at"] = datetime.now()
        await self.user_repo.update_user(user_id, fields_to_update) 

        return await self.user_repo.get_user_by_id(user_id)
    

    async def delete_user(self, current_user, user_id):
        user = await self.user_repo.get_user_by_id(user_id)

        self.validator.validate_user(user)
        self.validator.validate_role(current_user, user_id)

        await self.user_repo.delete_user(user_id)
        



        





