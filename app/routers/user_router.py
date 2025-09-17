from fastapi import APIRouter, Depends, status, Path, HTTPException, Query
from app.schemas.user_schema import UserRequest, UserUpdateRequest, UserOut
from app.repos.user_repo import UserRepo
from app.services.user_service import UserService
from app.core.dependencies import get_user_repo, get_user_service, get_current_user, role_checker





user_router = APIRouter(prefix="/users")


# ===================== GET all users =====================
@user_router.get("/", status_code=status.HTTP_200_OK)
async def get_all_users(limit: int = Query(10, ge=1, le=100),
                        offset: int = Query(0, ge=0), 
                        repo: UserRepo = Depends(get_user_repo),
                        current_user = Depends(get_current_user),
                        role_check = Depends(role_checker(["admin"]))):
    return await repo.get_all_users(limit, offset)





# ===================== GET users by id =====================
@user_router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id: int = Path(gt=0), 
                         service: UserService = Depends(get_user_service),
                         current_user = Depends(get_current_user),
                         role_check = Depends(role_checker(["user", "admin"]))):
    return await service.get_user_by_id(current_user, user_id)





# ===================== CREATE user =====================
@user_router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def create_user(user_data: UserRequest, 
                      service: UserService = Depends(get_user_service)):
    return await service.create_user(user_data.model_dump())






# ===================== UPDATE user =====================
@user_router.patch("/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(user_data: UserUpdateRequest, 
                      user_id: int = Path(gt=0), 
                      service: UserService = Depends(get_user_service),
                      current_user = Depends(get_current_user),
                      role_checker = Depends(role_checker(["user", "admin"]))):
    
    return await service.update_user(current_user, user_id, user_data.model_dump())




# ===================== DELETE user =====================
@user_router.delete("/{user_id}",  status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int = Path(gt=0),
                      service: UserService = Depends(get_user_service),
                      current_user = Depends(get_current_user),
                      role_checker = Depends(role_checker(["user", "admin"]))):
    await service.delete_user(current_user, user_id)





