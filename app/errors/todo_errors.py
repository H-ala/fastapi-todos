from app.errors.base import AppException

class TodoError(AppException):
    """Base class for user-related errors"""
    pass
 
class TodoNotFound(TodoError):
    """Todo not found"""
    pass

class TodoNothingToUpdate(TodoError):
    pass
