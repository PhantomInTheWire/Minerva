from typing import Dict, Any
from functools import wraps
from fastapi import HTTPException

class MinervaError(Exception):
    """Base error class for all Minerva application errors."""
    def __init__(self, message: str, details: Dict[str, Any] = None):
        """
        Initializes a MinervaError with a message and optional details.
        
        Args:
            message: A descriptive error message.
            details: Optional dictionary containing additional error context.
        """
        self.message = message
        self.details = details or {}
        super().__init__(self.message)

class APIError(MinervaError):
    """Base class for all API errors"""
    def __init__(self, message: str, original_error: Exception = None):
        """
        Initializes an APIError with a message and an optional original exception.
        
        Args:
            message: Description of the API error.
            original_error: The underlying exception that caused this error, if any.
        """
        super().__init__(message, {"original_error": str(original_error) if original_error else None})
        self.original_error = original_error

class ValidationError(MinervaError):
    """Raised when input validation fails."""
    pass

class DatabaseError(MinervaError):
    """Raised when database operations fail."""
    pass

class FileOperationError(MinervaError):
    """Raised when file operations (upload, processing, etc.) fail."""
    pass

class KnowledgeGraphError(MinervaError):
    """Raised when knowledge graph operations fail."""
    pass

class DocumentNotFoundError(DatabaseError):
    """Raised when a document is not found in the database"""
    pass

class ConverterInitializationError(ValidationError):
    """Raised when PDF converter fails to initialize"""
    pass

class FileProcessingError(FileOperationError):
    """Base class for file-related errors"""
    pass

class FileSaveError(FileProcessingError):
    """Raised when file saving fails"""
    pass

class FileDeleteError(FileProcessingError):
    """Raised when file deletion fails"""
    pass

class DatabaseCommitError(DatabaseError):
    """Raised when database commit operation fails"""
    pass

class PDFProcessingError(FileOperationError):
    """Raised when PDF text extraction fails"""
    pass

class InvalidFileTypeError(ValidationError):
    """Raised when invalid file type is uploaded"""
    pass

def format_error_response(error: Exception) -> Dict[str, Any]:
    """
    Formats an exception into a standardized dictionary for API error responses.
    
    If the exception is a MinervaError, includes its message and details; otherwise, returns the string representation of the error.
    """
    if isinstance(error, MinervaError):
        return {
            "status": "error",
            "message": error.message,
            "details": error.details
        }
    return {
        "status": "error",
        "message": str(error)
    }

def handle_api_errors(endpoint):
    """
    Decorator for asynchronous API endpoints that converts custom API errors into HTTP exceptions.
    
    Wraps an async endpoint function, catching `APIError` subclasses and raising `fastapi.HTTPException` with an appropriate status code:
    - 404 for `DocumentNotFoundError`
    - 400 for `InvalidFileTypeError` and `ConverterInitializationError`
    - 503 for `FileProcessingError` and `DatabaseCommitError`
    - 500 for other `APIError` instances
    
    The original exception is preserved as the cause of the HTTP exception.
    """

    @wraps(endpoint)
    async def wrapper(*args, **kwargs):
        """
        Wraps an asynchronous API endpoint to convert Minerva API errors into HTTP exceptions.
        
        Catches API-related exceptions and raises a FastAPI HTTPException with an appropriate
        status code and error message based on the specific error type.
        """
        try:
            return await endpoint(*args, **kwargs)
        except APIError as e:
            status_code = 500
            detail = e.message

            if isinstance(e, DocumentNotFoundError):
                status_code = 404
            elif isinstance(e, (InvalidFileTypeError, ConverterInitializationError)):
                status_code = 400
            elif isinstance(e, FileProcessingError):
                status_code = 503
            elif isinstance(e, DatabaseCommitError):
                status_code = 503

            raise HTTPException(
                status_code=status_code,
                detail=detail
            ) from e.original_error

    return wrapper