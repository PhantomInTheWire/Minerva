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
    """
    Extracts markdown-formatted text from a PDF file using fast extraction.
    
    Attempts to convert the PDF at the given file path to markdown using the
    `pymupdf4llm` library. Raises a `PDFProcessingError` if extraction fails.
    
    Args:
        file_path: Path to the PDF file.
    
    Returns:
        Extracted text in markdown format.
    
    Raises:
        PDFProcessingError: If text extraction fails.
    """
    try:
        return pymupdf4llm.to_markdown(file_path)
    except Exception as e:
        raise PDFProcessingError(f"Fast text extraction failed: {str(e)}") from e

async def process_pdf_slow(file_path: str) -> str:
    """
    Asynchronously extracts markdown-formatted text from a PDF file using external converter and rendering utilities.
    
    Attempts to obtain a converter instance and processes the PDF in executor threads to avoid blocking the event loop. Raises a ConverterInitializationError if the converter cannot be initialized. Wraps unexpected exceptions in an APIError, while re-raising known file processing errors.
    
    Args:
        file_path: Path to the PDF file to be processed.
    
    Returns:
        Extracted markdown-formatted text from the PDF.
    """
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