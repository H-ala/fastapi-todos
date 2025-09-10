from app.errors.base import AppException

class AuthError(AppException):
    """Base class for auth-related errors"""
    pass


class InvalidCredentials(AuthError):
    """User has provided wrong email or password during login"""
    pass

class RevokedToken(AuthError):
    """User has provided a token that has been revoked"""
    pass

class FieldRequired(AuthError):
    pass

class InvalidToken(AuthError):
    """User has provided invalid or expired token"""
    pass

class AccessTokenRequired(AuthError):
    """User has provided a refresh token when an access token is required"""
    pass

class InsufficientPermission(AuthError):
    """User does not have the necessary permission to perform this action"""
    pass