from ..middleware import logger
from ..db.main import SessionLocal
from datetime import datetime
from sqlmodel.ext.asyncio.session import AsyncSession
from ..db.models import PDFDocument
from fastapi import UploadFile
from .file_manager import save_pdf_file, remove_file
from .pdf_processor import extract_fast_text, process_pdf_slow
from ..error import (
    DocumentNotFoundError,
    DatabaseCommitError,
    FileProcessingError,
    APIError
)

async def run_slow_processing(document_id: str, file_path: str) -> str:
    """
    Processes a PDF file asynchronously, updates its content in the database, and removes the file.
    
    Retrieves a PDF document by ID, extracts text from the provided file path using a slow processing method, updates the document's content in the database, and deletes the temporary file after processing. Raises a `DocumentNotFoundError` if the document does not exist, and wraps unexpected errors in an `APIError`.
    
    Args:
        document_id: The unique identifier of the PDF document to update.
        file_path: The path to the PDF file to be processed.
    
    Returns:
        The extracted text content saved to the document.
    """
    async with SessionLocal() as session:
        try:
            document = await session.get(PDFDocument, document_id)
            if not document:
                raise DocumentNotFoundError(f"Document {document_id} not found")

            text = await process_pdf_slow(file_path)
            document.file_content = text
            session.add(document)
            await session.commit()
            logger.info(f"Slow processing completed for document {document_id}")
            return document.file_content

        except Exception as e:
            if not isinstance(e, FileProcessingError):
                raise APIError("Slow processing failed", original_error=e)
            raise
        finally:
            await remove_file(file_path)

async def create_document_record(session: AsyncSession, filename: str, content: str) -> PDFDocument:
    """
    Creates and commits a new PDFDocument record to the database.
    
    Adds a PDFDocument with the specified filename and extracted content, sets the current timestamp as the upload date, commits the transaction, and refreshes the instance to reflect the database state.
    
    Returns:
        The created PDFDocument instance.
    
    Raises:
        DatabaseCommitError: If the database commit fails.
    """
    try:
        doc = PDFDocument(
            name=filename,
            upload_date=datetime.now(),
            file_content=content
        )
        session.add(doc)
        await session.commit()
        await session.refresh(doc)
        return doc
    except Exception as e:
        await session.rollback()
        raise DatabaseCommitError("Failed to create document record") from e

async def full_upload_process(file: UploadFile, session: AsyncSession) -> tuple[PDFDocument, str]:
    """
    Handles the complete process of saving an uploaded PDF, extracting its text, and creating a database record.
    
    Args:
        file: The uploaded PDF file to process.
        session: The asynchronous database session for record creation.
    
    Returns:
        A tuple containing the created PDFDocument instance and the file path of the saved PDF.
    
    Raises:
        FileProcessingError: If any error occurs during file saving, text extraction, or database record creation.
    """
    try:
        file_path = await save_pdf_file(file)
        fast_text = extract_fast_text(file_path)
        document = await create_document_record(session, file.filename, fast_text)
        return document, file_path
    except Exception as e:
        raise FileProcessingError(f"Error in processing file: {str(e)}") from e
