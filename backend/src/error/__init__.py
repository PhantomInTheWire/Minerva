from typing import Dict, Any
from functools import wraps
from fastapi import HTTPException

class MinervaError(Exception):
    """Base error class for all Minerva application errors."""
    def __init__(self, message: str, details: Dict[str, Any] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)

class APIError(MinervaError):
    """Base class for all API errors"""
    def __init__(self, message: str, original_error: Exception = None):
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
    """Formats an error into a consistent API response structure."""
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
            elif isinstance(e, DatabaseCommitError):
                status_code = 503

            raise HTTPException(
                status_code=status_code,
                detail=detail
            ) from e.original_error

    return wrapper