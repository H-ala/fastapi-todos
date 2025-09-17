from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from app.services.auth_service import AuthService
from app.schemas.auth_schema import LoginRequest
from app.utils.security import create_access_token, create_refresh_token
from app.core.dependencies import get_auth_service, get_current_user
from app.schemas.auth_schema import RefreshTokenRequest
from app.schemas.user_schema import UserRequest





auth_router = APIRouter(prefix="/auth")



# ===================== GET access token =====================
@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def get_all_users(login_data: LoginRequest, 
                        service: AuthService = Depends(get_auth_service)):
    user_data = await service.authenticate_user(
        username=login_data.username,
        email=login_data.email,
        password=login_data.password
    )

    access_token = create_access_token(dict(user_data))
    refresh_token = create_refresh_token()

    await service.save_refresh_token(refresh_token, user_data["id"])



    return JSONResponse(
                content={
                    "massage": "login successful",
                    "token_type": "bearer",
                    "access_token": access_token,
                    "refresh_token": refresh_token
                }
            )


@auth_router.post("/refresh_token", status_code=status.HTTP_200_OK)
async def get_net_access_token(refresh_token: RefreshTokenRequest,
                               service: AuthService = Depends(get_auth_service)):
    
    new_access_token = await service.verify_refresh_token(refresh_token.refresh_token)
    return JSONResponse(
        content={
            "access_token": new_access_token
        }
    )


@auth_router.get("/logout", status_code=status.HTTP_200_OK)
async def revoke_token(user_data: UserRequest = Depends(get_current_user),
                       service: AuthService = Depends(get_auth_service)):
    await service.log_out(user_data["id"])

    return JSONResponse(
        content={
            "message": "user logged out seccussfully"
        }
    )
