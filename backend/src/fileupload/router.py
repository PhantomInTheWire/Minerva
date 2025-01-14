import pymupdf4llm
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from ..db.models import PDFDocument
from ..db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
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
    """
    Perform a simple health check for the service.
    
    Returns:
        dict: A dictionary with a health status indicator, confirming the service is operational.
    """
    return {"health": "positive"}


@upload_router.post("/documents", response_model=PDFDocument, status_code=201)
async def create_document(
        file: UploadFile = File(...),
        session: AsyncSession = Depends(get_session)
):
    """
        Create a new PDF document from an uploaded file.
        
        Asynchronously processes a PDF file upload, extracts text and metadata, and saves the document to the database.
        
        Parameters:
            file (UploadFile): The uploaded PDF file to be processed.
            session (AsyncSession): Database session for storing the document.
        
        Returns:
            PDFDocument: The created document with extracted text and metadata.
        
        Raises:
            HTTPException: 
                - 400 if the uploaded file is not a PDF
                - 500 if PDF converter fails to initialize or processing encounters an error
        
        Notes:
            - Saves the uploaded file temporarily in an 'uploads' directory
            - Uses a unique filename to prevent conflicts
            - Processes file in 64KB chunks for memory efficiency
            - Automatically deletes the temporary file after processing
            - Logs any errors encountered during file processing
        """
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


@upload_router.get("/documents/fast", response_model=PDFDocument, status_code=200)
async def get_document(
        file: UploadFile = File(...),
        session: AsyncSession = Depends(get_session)
):
    """
        Asynchronously process and save a PDF document to the database using fast markdown conversion.
        
        Parameters:
            file (UploadFile): The uploaded PDF file to be processed
            session (AsyncSession): Database session for storing the document
        
        Raises:
            HTTPException: If the uploaded file is not a PDF
        
        Notes:
            - Saves the uploaded PDF file temporarily in the 'uploads' directory
            - Converts PDF to markdown using pymupdf4llm
            - Creates a PDFDocument with the file's name, upload date, and markdown content
            - Schedules the temporary file for deletion after processing
        """
        if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    unique_filename = f"{uuid4()}_{file.filename}"
    file_path = os.path.join(upload_dir, unique_filename)
    async with aiofiles.open(file_path, "wb") as buffer:
        chunk_size = 64 * 1024  # 64KB chunks
        while chunk := await file.read(chunk_size):
            await buffer.write(chunk)

    text = pymupdf4llm.to_markdown(file_path)
    pdf_document = PDFDocument(
        name=file.filename,
        upload_date=datetime.now(),
        file_content=text
    )
    session.add(pdf_document)
    await session.commit()
    background_tasks = BackgroundTasks()
    background_tasks.add_task(os.remove, file_path)
    return


