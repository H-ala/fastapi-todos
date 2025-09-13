from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.schemas.todo_schema import TodoRequest, TodoUpdateRequest

class TodoRepo:
    def __init__(self, db: AsyncSession):
        self.db = db
        


    async def get_all_todos(self, user_id, limit: int, offset: int):
        query = text("SELECT * FROM todos WHERE user_id = :user_id ORDER BY id LIMIT :limit OFFSET :offset;")
        result = await self.db.execute(query, {"user_id": user_id, "limit": limit, "offset": offset})
        return result.mappings().all()



    async def get_todo_by_id(self, todo_id: int):
        query = text("SELECT * FROM todos WHERE id = :id")
        result = await self.db.execute(query, {"id": todo_id})
        return result.mappings().first() # None if not found



    async def create_todo(self, todo_req: TodoRequest, user_id: int):
        query = text(
            """
            INSERT INTO todos (title, description, priority, complete, user_id)
            VALUES (:title, :description, :priority, :complete, :user_id)
            RETURNING *;
            """
        )

        data = {**todo_req.model_dump(), "user_id": user_id}
        result = await self.db.execute(query, data)
        await self.db.commit()
        return result.mappings().first()



    async def update_todo(self, todo_id: int, todo_data: TodoUpdateRequest):

        set_clause = ", ".join([f"{key} = :{key}" for key in todo_data.keys()])
        query = text(f"UPDATE todos SET {set_clause} WHERE id = :id")
        data = {**todo_data, "id": todo_id}

        await self.db.execute(query, data)
        await self.db.commit()
        return 
 

    async def delete_todo(self, todo_id: int):
        await self.db.execute(text("DELETE FROM todos WHERE id = :id;"), {"id": todo_id})
        await self.db.commit()
        return 

