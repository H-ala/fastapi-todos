from app.errors.base import AppException

class UserError(AppException):
    """Base class for user-related errors"""
    pass
 
class UserNotFound(UserError):
    """User not found"""
    pass

class EmailAlreadyExists(UserError):
    """Email already exists"""
    pass

class UsernameAlreadyExists(UserError):
    """Username already exists"""
    pass

class PasswordMismatch(UserError):
    """Passwords do not match"""
    pass

class PasswordAlreadySet(UserError):
    """New password is same as old password"""
    pass

class UserNothingToUpdate(UserError):
    pass