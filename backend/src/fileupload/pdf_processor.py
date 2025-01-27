from marker.output import text_from_rendered
from ..error import (
    ConverterInitializationError,
    PDFProcessingError,
    FileProcessingError,
    APIError
)
from ..converter import get_converter
from ..middleware import logger
import asyncio
import pymupdf4llm

def extract_fast_text(file_path: str) -> str:
    """Extract text using pymupdf4llm (fast)"""
    try:
        return pymupdf4llm.to_markdown(file_path)
    except Exception as e:
        raise PDFProcessingError(f"Fast text extraction failed: {str(e)}") from e

async def process_pdf_slow(file_path: str) -> str:
    """Converts pdf to markdown slowly but reliably using marker/surya libs/models"""
    try:
        converter = get_converter()
        if not converter:
            raise ConverterInitializationError("PDF converter not initialized")

        rendered = await asyncio.get_event_loop().run_in_executor(
            None, converter, file_path
        )

        text, metadata, images = await asyncio.get_event_loop().run_in_executor(
            None, text_from_rendered, rendered
        )

        logger.info(f"Slow processing completed for file {file_path}")
        return text

    except Exception as e:
        if not isinstance(e, FileProcessingError):
            raise APIError("Slow processing failed", original_error=e)
        raise