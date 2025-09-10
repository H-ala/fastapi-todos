from fastapi import APIRouter, Depends, status, Path, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.repos.todo_repo import TodoRepo
from app.schemas.todo_schema import TodoRequest, TodoUpdateRequest
from app.core.dependencies import get_todo_repo, role_checker



todo_router = APIRouter(prefix="/todos")




# ===================== GET all todos =====================
@todo_router.get("/todos", status_code=status.HTTP_200_OK)
async def get_all_todos(limit: int = Query(10, ge=1, le=100),
                        offset: int = Query(0, ge=0), 
                        repo: TodoRepo = Depends(get_todo_repo),
                        role_check = Depends(role_checker(["user, admin"]))):
    return await repo.get_all_todos(limit, offset)



# ===================== GET todo by id =====================
@todo_router.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todo_by_id(todo_id: int = Path(gt=0), repo: TodoRepo = Depends(get_todo_repo)):
    todo = await repo.get_todo_by_id(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo



# ===================== CREATE todo =====================
@todo_router.post("/todos", status_code=status.HTTP_201_CREATED)
async def create_todo(todo_req: TodoRequest, repo: TodoRepo = Depends(get_todo_repo)):
    return await repo.create_todo(todo_req)



# ===================== UPDATE todo =====================
@todo_router.patch("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def update_todo(todo_req: TodoUpdateRequest, todo_id: int = Path(gt=0), repo: TodoRepo = Depends(get_todo_repo)):
    updated_todo = await repo.update_todo(todo_req, todo_id)
    if updated_todo is None:
        existing_todo = await repo.get_todo_by_id(todo_id)
        if existing_todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        else:
            raise HTTPException(status_code=400, detail="No fields provided for update")



# ===================== DELETE todo =====================
@todo_router.delete("/todos/{todo_id}",  status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int = Path(gt=0), repo: TodoRepo = Depends(get_todo_repo)):
   to_be_deleted = await repo.delete_todo(todo_id)
   if not to_be_deleted:
       raise HTTPException(status_code=404, detail="Todo not found")
   return




