from ..error import PDFProcessingError, FileProcessingError, APIError
from ..middleware import logger
import pymupdf4llm

def extract_fast_text(file_path: str) -> str:
    """Extract text using pymupdf4llm (fast)"""
    try:
        return pymupdf4llm.to_markdown(file_path)
    except Exception as e:
        raise PDFProcessingError(f"Fast text extraction failed: {str(e)}") from e

async def process_pdf_slow(file_path: str) -> str:
    """Fallback PDF extraction using the same markdown converter."""
    try:
        text = extract_fast_text(file_path)
        logger.info(f"Fallback processing completed for file {file_path}")
        return text

    except Exception as e:
        if not isinstance(e, FileProcessingError):
            raise APIError("Slow processing failed", original_error=e)
        raise
