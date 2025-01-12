from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from ..db.models import PDFDocument
from ..db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
import shutil
import os
from datetime import datetime
from uuid import uuid4
from marker.output import text_from_rendered

upload_router = APIRouter()


@upload_router.get("/", response_model=dict)
async def health_check():
    return {"health": "positive"}


@upload_router.post("/documents/", response_model=PDFDocument, status_code=201)
async def create_document(
        file: UploadFile = File(...),
        session: AsyncSession = Depends(get_session)
):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    unique_filename = f"{uuid4()}_{file.filename}"
    file_path = os.path.join(upload_dir, unique_filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        rendered = converter(file_path)
        text, metadata, images = text_from_rendered(rendered)

        pdf_document = PDFDocument(
            name=file.filename,
            upload_date=datetime.now(),
            file_content=text
        )

        session.add(pdf_document)
        await session.commit()
        await session.refresh(pdf_document)
        return pdf_document

    except Exception as _:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail="An error occurred during file processing.")
