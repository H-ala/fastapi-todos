from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.schemas.todo_schema import TodoRequest, TodoUpdateRequest

class TodoRepo:
    def __init__(self, db: AsyncSession):
        self.db = db
        


    async def get_all_todos(self, limit: int, offset: int):
        query = text("SELECT * FROM todos ORDER BY id LIMIT :limit OFFSET :offset;")
        result = await self.db.execute(query, {"limit": limit, "offset": offset})
        return result.mappings().all()



    async def get_todo_by_id(self, todo_id: int):
        query = text("SELECT * FROM todos WHERE id = :id")
        result = await self.db.execute(query, {"id": todo_id})
        return result.mappings().first() # None if not found



    async def create_todo(self, todo_req: TodoRequest):
        query = text(
            """
            INSERT INTO todos (title, description, priority, complete)
            VALUES (:title, :description, :priority, :complete)
            RETURNING *;
            """
        )

        result = await self.db.execute(query, todo_req.model_dump())
        await self.db.commit()
        return result.mappings().first()



    async def update_todo(self, todo_req: TodoUpdateRequest, todo_id: int):
        fields_to_update = {k: v for k, v in todo_req.model_dump().items() if v is not None}
        if not fields_to_update:
            return None
        
        # this below line creates: 
        #         title = :title,   
        #         description = :description,
        #         priority = :priority,
        #         complete = :complete
        set_clause = ", ".join([f"{key} = :{key}" for key in fields_to_update.keys()])
        query = text(f"UPDATE todos SET {set_clause} WHERE id = :id")
        data = {**fields_to_update, "id": todo_id}

        await self.db.execute(query, data)
        await self.db.commit()
        return await self.get_todo_by_id(todo_id)

 

    async def delete_todo(self, todo_id: int):
        result = await self.db.execute(text("DELETE FROM todos WHERE id = :id;"), {"id": todo_id})
        await self.db.commit()
        return result.rowcount # number of deleted rows

