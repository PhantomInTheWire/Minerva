from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from backend.src.db.models import PDFDocument
from backend.src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import Session, select
import shutil
import os
from datetime import datetime
from uuid import uuid4

upload_router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_upload_file(upload_file: UploadFile) -> str:
    """Save uploaded file to disk and return the file path"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_filename = f"{timestamp}_{uuid4().hex}_{upload_file.filename}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    return file_path


@upload_router.get("/")
async def health_check():
    return {"health": "positive"}


@upload_router.post("/documents/", response_model=PDFDocument, status_code=201)
async def create_document(
        name: str,
        description: str | None = None,
        file: UploadFile = File(...),
        session: AsyncSession = Depends(get_session)
):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    file_path = save_upload_file(file)

    document = PDFDocument(
        name=name,
        description=description,
        file_path=file_path
    )

    session.add(document)
    await session.commit()
    await session.refresh(document)
    return document


@upload_router.get("/documents/", response_model=List[PDFDocument])
async def read_documents(session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(PDFDocument))
    documents = result.all()
    return documents


@upload_router.get("/documents/{document_id}", response_model=PDFDocument)
async def read_document(document_id: str, session: AsyncSession = Depends(get_session)):
    document = await session.get(PDFDocument, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document

@upload_router.delete("/documents/{document_id}", status_code=204)
async def delete_document(document_id: str, session: AsyncSession = Depends(get_session)):
    document = await session.get(PDFDocument, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    if os.path.exists(document.file_path):
        os.remove(document.file_path)

    await session.delete(document)
    await session.commit()
    return None