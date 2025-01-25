from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks
from sqlmodel.ext.asyncio.session import AsyncSession
from .error import handle_api_errors, InvalidFileTypeError
from .service import run_slow_processing, full_upload_process
from ..db.main import get_session
from ..db.models import PDFDocument
from ..middleware import logger

upload_router = APIRouter()

@upload_router.post("/documents/", response_model=PDFDocument, status_code=201)
@handle_api_errors  # Apply the decorator here
async def create_document(
        file: UploadFile = File(...),
        session: AsyncSession = Depends(get_session),
        background_tasks: BackgroundTasks = BackgroundTasks(),
):
    if not file.filename.lower().endswith('.pdf'):
        raise InvalidFileTypeError("Only PDF files allowed")

    try:
        doc, path = await full_upload_process(file, session)
        background_tasks.add_task(run_slow_processing, doc.id, path)
        return doc
    except Exception as e:
        logger.error(f"Upload failed: {str(e)}")
        raise