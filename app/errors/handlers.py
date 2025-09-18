# app/errors/handlers.py
from typing import Any, Callable
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.errors.user_errors import (
    UserNotFound, EmailAlreadyExists, UsernameAlreadyExists,
    PasswordMismatch, PasswordAlreadySet, UserNothingToUpdate
)

from app.errors.auth_errors import (
    InvalidCredentials, RevokedToken, InvalidToken,
    AccessTokenRequired, InsufficientPermission
)

from app.errors.todo_errors import (
    TodoNotFound, TodoNothingToUpdate
)

def create_exception_handler(status_code: int, initial_details: Any) -> Callable[[Request, Exception], JSONResponse]:
    async def exception_handler(request: Request, exc: Exception):
        # می‌توان پیام دقیق‌تر یا dynamic هم داد:
        content = initial_details.copy()
        content["detail"] = str(exc)  # پیام واقعی خطا
        return JSONResponse(content=content, status_code=status_code)
    return exception_handler

def register_all_errors(app: FastAPI):
    app.add_exception_handler(
        UserNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_details={"message": "User not found", "error_code": "user_not_found"}
        )
    )
    app.add_exception_handler(
        EmailAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_409_CONFLICT,
            initial_details={"message": "Email already exists", "error_code": "email_exists"}
        )
    )
    app.add_exception_handler(
        UsernameAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_409_CONFLICT,
            initial_details={"message": "Username already exists", "error_code": "username_exists"}
        )
    )
    app.add_exception_handler(
        PasswordMismatch,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_details={"message": "Passwords do not match", "error_code": "password_mismatch"}
        )
    )
    app.add_exception_handler(
        PasswordAlreadySet,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_details={"message": "Password is already set", "error_code": "password_already_set"}
        )
    )
    
    app.add_exception_handler(
        UserNothingToUpdate,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_details={"message": "No fields provided for update", "error_code": "nothing_to_update"}
        )
    )

    app.add_exception_handler(
        TodoNothingToUpdate,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_details={"message": "No fields provided for update", "error_code": "nothing_to_update"}
        )
    )

    app.add_exception_handler(
        InvalidCredentials,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_details={
                "message": "Invalid email or password.",
                "error_code": "invalid_email_or_password"
            }
        )
    )

    app.add_exception_handler(
        RevokedToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_details={
                "message": "Token is invalid or has been revoked",
                "resolution": "Please get new token",
                "error_code": "token_revoked"
            }
        )
    )
    app.add_exception_handler(
        InvalidToken,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_details={
                "message": "Token is invalid or expired",
                "resolution": "Please get new token",
                "error_code": "invalid_token"
            }
        )
    )
    app.add_exception_handler(
        AccessTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_details={
                "message": "Please provide a valid access token",
                "resolution": "Please get an access token",
                "error_code": "access_token_needed"
            }
        )
    )

    app.add_exception_handler(
        InsufficientPermission,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_details={
                "message": "you are not allowed to perform this action",
                "error_code": "permission_denied"
            }
        )
    )

    app.add_exception_handler(
        TodoNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_details={"message": "Todo not found", "error_code": "todo_not_found"}
        )
    )



    # خطای عمومی سرور
    @app.exception_handler(500)
    async def internal_server_error(request: Request, exc: Exception):
        return JSONResponse(
            content={"message": "Internal server error", "error_code": "server_error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    # خطای دیتابیس
    @app.exception_handler(SQLAlchemyError)
    async def database_error(request: Request, exc: Exception):
        return JSONResponse(
            content={"message": "Database error", "error_code": "database_error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
