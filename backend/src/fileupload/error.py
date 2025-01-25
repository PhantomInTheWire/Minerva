from functools import wraps
from fastapi import HTTPException


class APIError(Exception):
    """Base class for all API errors"""

    def __init__(self, message: str, original_error: Exception = None):
        self.message = message
        self.original_error = original_error
        super().__init__(message)


class DocumentNotFoundError(APIError):
    """Raised when a document is not found in the database"""
    pass


class ConverterInitializationError(APIError):
    """Raised when PDF converter fails to initialize"""
    pass


class FileProcessingError(APIError):
    """Base class for file-related errors"""
    pass


class FileSaveError(FileProcessingError):
    """Raised when file saving fails"""
    pass


class FileDeleteError(FileProcessingError):
    """Raised when file deletion fails"""
    pass


class DatabaseError(APIError):
    """Base class for database-related errors"""
    pass


class DatabaseCommitError(DatabaseError):
    """Raised when database commit operation fails"""
    pass


class PDFProcessingError(APIError):
    """Raised when PDF text extraction fails"""
    pass


class InvalidFileTypeError(APIError):
    """Raised when invalid file type is uploaded"""
    pass


def handle_api_errors(endpoint):
    """Decorator to handle API errors and convert them to HTTP responses."""

    @wraps(endpoint)
    async def wrapper(*args, **kwargs):
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
            elif isinstance(e, DatabaseError):
                status_code = 503

            raise HTTPException(
                status_code=status_code,
                detail=detail
            ) from e.original_error

    return wrapper
