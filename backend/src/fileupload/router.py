from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from ..db.models import PDFDocument
from ..db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
import shutil
import os
from datetime import datetime
from uuid import uuid4
from marker.output import text_from_rendered
from ..converter import get_converter
import aiofiles
import asyncio
from fastapi import BackgroundTasks
from ..middleware import logger

upload_router = APIRouter()


@upload_router.get("/", response_model=dict)
async def health_check():
    return {"health": "positive"}


@upload_router.post("/documents", response_model=PDFDocument, status_code=201)
async def create_document(
        file: UploadFile = File(...),
        session: AsyncSession = Depends(get_session)
):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    # Initialize converter outside of request handling
    converter = get_converter()
    if converter is None:
        raise HTTPException(status_code=500, detail="PDF converter not initialized")

    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    unique_filename = f"{uuid4()}_{file.filename}"
    file_path = os.path.join(upload_dir, unique_filename)

    try:
        async with aiofiles.open(file_path, "wb") as buffer:
            chunk_size = 64 * 1024  # 64KB chunks
            while chunk := await file.read(chunk_size):
                await buffer.write(chunk)

        rendered = await asyncio.get_event_loop().run_in_executor(
            None, converter, file_path
        )

        # Process text extraction in thread pool
        text, metadata, images = await asyncio.get_event_loop().run_in_executor(
            None, text_from_rendered, rendered
        )

        pdf_document = PDFDocument(
            name=file.filename,
            upload_date=datetime.now(),
            file_content=text
        )

        session.add(pdf_document)
        await session.commit()

        background_tasks = BackgroundTasks()
        background_tasks.add_task(os.remove, file_path)

        return pdf_document

    except Exception as e:
        logger.error(f"Error processing PDF: {str(e)}")
        if os.path.exists(file_path):
            await asyncio.get_event_loop().run_in_executor(None, os.remove, file_path)
        raise HTTPException(status_code=500, detail="An error occurred during file processing.")
