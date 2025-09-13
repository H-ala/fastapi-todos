from fastapi import APIRouter, Depends, status, Path, HTTPException, Query
from app.schemas.todo_schema import TodoRequest, TodoUpdateRequest
from app.core.dependencies import get_todo_service, role_checker, get_current_user
from app.services.todo_service import TodoService



todo_router = APIRouter(prefix="/todos")




# ===================== GET all todos =====================
@todo_router.get("/", status_code=status.HTTP_200_OK)
async def get_all_todos(limit: int = Query(10, ge=1, le=100),
                        offset: int = Query(0, ge=0), 
                        service: TodoService = Depends(get_todo_service),
                        current_user = Depends(get_current_user),
                        role_check = Depends(role_checker(["user", "admin"]))):
    return await service.get_all_todos(current_user.id, limit, offset)



# ===================== GET todo by id =====================
@todo_router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todo_by_id(todo_id: int = Path(gt=0),
                         service: TodoService = Depends(get_todo_service),
                         current_user = Depends(get_current_user),
                         role_checker = Depends(role_checker(["user", "admin"]))):
    return await service.get_todo_by_id(current_user, todo_id)



# ===================== CREATE todo =====================
@todo_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_todo(todo_req: TodoRequest, 
                      service: TodoService = Depends(get_todo_service),
                      current_user = Depends(get_current_user),
                      role_checker = Depends(role_checker(["user", "admin"]))
                      ):
    return await service.create_todo(current_user, todo_req)



# ===================== UPDATE todo =====================
@todo_router.patch("/{todo_id}", status_code=status.HTTP_200_OK)
async def update_todo(todo_req: TodoUpdateRequest, todo_id: int = Path(gt=0), 
                      service: TodoService = Depends(get_todo_service),
                      current_user = Depends(get_current_user),
                      role_checker = Depends(role_checker(["user", "admin"]))
                      ):
    
    return await service.update_todo(current_user, todo_req.model_dump(), todo_id)



# ===================== DELETE todo =====================
@todo_router.delete("/{todo_id}",  status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int = Path(gt=0), 
                      service: TodoService = Depends(get_todo_service),
                      current_user = Depends(get_current_user),
                      role_checker = Depends(role_checker(["user", "admin"]))):

    await service.delete_todo(current_user, todo_id)





