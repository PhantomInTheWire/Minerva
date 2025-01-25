import pymupdf4llm
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks
from ..db.models import PDFDocument
from ..db.main import get_session, SessionLocal
from sqlmodel.ext.asyncio.session import AsyncSession
import os
from datetime import datetime
from uuid import uuid4
from marker.output import text_from_rendered
from ..converter import get_converter
import aiofiles
import asyncio
from ..middleware import logger

upload_router = APIRouter()

async def run_slow_processing(document_id: int, file_path: str):
    async with SessionLocal() as session:
        try:
            document = await session.get(PDFDocument, document_id)
            if not document:
                logger.error(f"Document {document_id} not found for slow processing")
                return

            converter = get_converter()
            if not converter:
                logger.error("PDF converter not initialized in slow processing")
                return

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
            logger.error(f"Error during slow processing of document {document_id}: {str(e)}")
            await session.rollback()
        finally:
            if os.path.exists(file_path):
                try:
                    await asyncio.get_event_loop().run_in_executor(None, os.remove, file_path)
                except Exception as e:
                    logger.error(f"Error deleting file {file_path}: {str(e)}")

@upload_router.post("/documents/", response_model=PDFDocument, status_code=201)
async def create_document(
        file: UploadFile = File(...),
        session: AsyncSession = Depends(get_session),
        background_tasks: BackgroundTasks = BackgroundTasks(),
):
    """
    first creates a new PDF document using a fast lib(pymupdf) then does slow processing
    using marker/surya for accurate equations/tables etc.
    """
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    unique_filename = f"{uuid4()}_{file.filename}"
    file_path = os.path.join(upload_dir, unique_filename)

    try:
        async with aiofiles.open(file_path, "wb") as buffer:
            chunk_size = 64 * 1024  # 64KB chunks
            while chunk := await file.read(chunk_size):
                await buffer.write(chunk)

        fast_text = pymupdf4llm.to_markdown(file_path)
        pdf_document = PDFDocument(
            name=file.filename,
            upload_date=datetime.now(),
            file_content=fast_text
        )

        session.add(pdf_document)
        await session.commit()
        await session.refresh(pdf_document)

        background_tasks.add_task(run_slow_processing, pdf_document.id, file_path)
        return pdf_document

    except Exception as e:
        logger.error(f"Error in fast processing: {str(e)}")
        if os.path.exists(file_path):
            await asyncio.get_event_loop().run_in_executor(None, os.remove, file_path)
        raise HTTPException(status_code=500, detail="Error processing file")