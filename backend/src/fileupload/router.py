from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks
from sqlmodel.ext.asyncio.session import AsyncSession
from ..error import handle_api_errors, InvalidFileTypeError, FileProcessingError
from .service import run_slow_processing, full_upload_process
from ..db.main import get_session
from ..db.models import PDFDocument
from ..knowledge_graphs.router import markdown_to_neo4j_kg
from ..middleware import logger

upload_router = APIRouter()

@upload_router.post("/documents/", response_model=PDFDocument, status_code=201)
@handle_api_errors
async def create_document(
        file: UploadFile = File(...),
        session: AsyncSession = Depends(get_session),
        background_tasks: BackgroundTasks = BackgroundTasks(),
):
    """
        Creates a new PDF document from an uploaded file.
        
        Validates that the uploaded file is a PDF, processes and stores it in the database, and returns the created document. Raises an error if the file type is invalid or if processing fails.
        """
    if not file.filename.lower().endswith('.pdf'):
        raise InvalidFileTypeError("Only PDF files allowed")

    try:
        doc, path = await full_upload_process(file, session)
        
        async def process_and_create_kg(doc_id: str, file_path: str):
            """
            Processes a document to generate markdown content for knowledge graph creation.
            
            Awaits slow processing of the document and file path to produce markdown content, which can be used for further knowledge graph generation.
            """
            markdown_content = await run_slow_processing(doc_id, file_path)
            # logger.info(await markdown_to_neo4j_kg(markdown_content))
            
        # background_tasks.add_task(process_and_create_kg, doc.id, path)
        return doc
    except Exception as e:
        raise FileProcessingError(f"Error in processing file: {str(e)}") from e
