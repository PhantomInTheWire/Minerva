from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks
from sqlmodel.ext.asyncio.session import AsyncSession
from .error import handle_api_errors, InvalidFileTypeError, FileProcessingError
from .service import run_slow_processing, full_upload_process
from ..db.main import get_session
from ..db.models import PDFDocument
from ..knowledge_graphs.router import markdown_to_neo4j_kg

upload_router = APIRouter()

@upload_router.post("/documents/", response_model=PDFDocument, status_code=201)
@handle_api_errors
async def create_document(
        file: UploadFile = File(...),
        session: AsyncSession = Depends(get_session),
        background_tasks: BackgroundTasks = BackgroundTasks(),
):
    """
    Create a new PDF document.
    converts pdf to markdown and saves it to the db.
    """
    if not file.filename.lower().endswith('.pdf'):
        raise InvalidFileTypeError("Only PDF files allowed")

    try:
        doc, path = await full_upload_process(file, session)
        
        async def process_and_create_kg(doc_id: str, file_path: str):
            markdown_content = await run_slow_processing(doc_id, file_path)
            await markdown_to_neo4j_kg(markdown_content)
            
        background_tasks.add_task(process_and_create_kg, doc.id, path)
        return doc
    except Exception as e:
        raise FileProcessingError(f"Error in processing file: {str(e)}") from e
