from app.repos.todo_repo import TodoRepo
from app.errors.todo_errors import (
    TodoNotFound, TodoNothingToUpdate
)
from app.errors.auth_errors import (
    InsufficientPermission
)
from datetime import datetime



class TodoValidator:
    def __init__(self, todo_repo: TodoRepo):
        self.todo_repo = todo_repo

    @staticmethod
    def validate_todo(todo):
        if todo is None:
            raise TodoNotFound(f"Todo not found")
        
    @staticmethod
    def validate_role(current_user, todo):
        if not current_user.id == todo.user_id and current_user.role == 'user':
            raise InsufficientPermission()



class TodoService:
    def __init__(self, todo_repo: TodoRepo,
                 validator: TodoValidator = None):
        self.todo_repo = todo_repo
        self.validator = validator or TodoValidator(todo_repo)


    async def get_all_todos(self, user_id, limit, offset):
        return await self.todo_repo.get_all_todos(user_id, limit, offset)


    async def get_todo_by_id(self, current_user, todo_id):
        todo = await self.todo_repo.get_todo_by_id(todo_id)
        self.validator.validate_todo(todo)
        self.validator.validate_role(current_user, todo)
        return todo    


    async def create_todo(self, current_user, todo_data):

        return await self.todo_repo.create_todo(todo_data, current_user.id)


    async def update_todo(self, current_user, todo_data, todo_id):
        todo = await self.todo_repo.get_todo_by_id(todo_id)

        self.validator.validate_todo(todo)
        self.validator.validate_role(current_user, todo)
        fields_to_update = {k: v for k, v in todo_data.items() if v is not None}

        if not fields_to_update:
            raise TodoNothingToUpdate("No fields provided for update")


        fields_to_update["updated_at"] = datetime.now()
        await self.todo_repo.update_todo(todo_id, fields_to_update) 

        return await self.todo_repo.get_todo_by_id(todo_id)
    

    async def delete_todo(self, current_user, todo_id):
        todo = await self.todo_repo.get_todo_by_id(todo_id)

        self.validator.validate_todo(todo)
        self.validator.validate_role(current_user, todo)

        await self.todo_repo.delete_todo(todo_id)