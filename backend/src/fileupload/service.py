from marker.output import text_from_rendered
from .error import (
    DocumentNotFoundError,
    ConverterInitializationError,
    FileSaveError,
    FileDeleteError,
    DatabaseCommitError,
    PDFProcessingError,
    APIError
)
from ..converter import get_converter
from ..middleware import logger
from ..db.main import SessionLocal
import asyncio
import pymupdf4llm
import aiofiles
import os
from datetime import datetime
from sqlmodel.ext.asyncio.session import AsyncSession
from ..db.models import PDFDocument
from fastapi import UploadFile
from uuid import uuid4

async def run_slow_processing(document_id: str, file_path: str):
    async with SessionLocal() as session:
        try:
            document = await session.get(PDFDocument, document_id)
            if not document:
                raise DocumentNotFoundError(f"Document {document_id} not found")

            converter = get_converter()
            if not converter:
                raise ConverterInitializationError("PDF converter not initialized")

            rendered = await asyncio.get_event_loop().run_in_executor(
                None, converter, file_path
            )

            text, metadata, images = await asyncio.get_event_loop().run_in_executor(
                None, text_from_rendered, rendered
            )

            document.file_content = text
            session.add(document)
            await session.commit()
            logger.info(f"Slow processing completed for document {document_id}")

        except Exception as e:
            if not isinstance(e, APIError):
                raise APIError("Slow processing failed", original_error=e)
            raise
        finally:
            await remove_file(file_path)

async def remove_file(file_path: str):
    if os.path.exists(file_path):
        try:
            await asyncio.get_event_loop().run_in_executor(None, os.remove, file_path)
        except Exception as e:
            raise FileDeleteError(f"Error deleting file {file_path}") from e

async def save_pdf_file(file: UploadFile) -> str:
    """Save uploaded PDF file with UUID prefix"""
    try:
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, f"{uuid4()}_{file.filename}")
        async with aiofiles.open(file_path, "wb") as buffer:
            await file.seek(0)
            while content := await file.read(64 * 1024):
                await buffer.write(content)
        return file_path
    except Exception as e:
        raise FileSaveError(f"Failed to save file: {str(e)}") from e

async def create_document_record(session: AsyncSession, filename: str, content: str) -> PDFDocument:
    """Create and commit PDFDocument record"""
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

def extract_fast_text(file_path: str) -> str:
    """Extract text using pymupdf4llm (fast)"""
    try:
        return pymupdf4llm.to_markdown(file_path)
    except Exception as e:
        raise PDFProcessingError(f"Fast text extraction failed: {str(e)}") from e

async def full_upload_process(file: UploadFile, session: AsyncSession) -> tuple[PDFDocument, str]:
    """Full upload processing pipeline"""
    try:
        file_path = await save_pdf_file(file)
        fast_text = extract_fast_text(file_path)
        document = await create_document_record(session, file.filename, fast_text)
        return document, file_path
    except Exception as e:
        logger.error(f"Error during processing of file {str(e)}")
        raise