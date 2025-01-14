from contextlib import asynccontextmanager
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from fastapi import FastAPI
from .fileupload.router import upload_router
from .middleware import register_middleware
from .converter import init_converter

version="v1"

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage the lifecycle of the FastAPI application, initializing and cleaning up resources.
    
    This asynchronous context manager is responsible for setting up and tearing down application-wide resources, specifically initializing the document converter.
    
    Yields control back to the FastAPI application after initialization, allowing for graceful startup and shutdown processes.
    
    Args:
        app (FastAPI): The FastAPI application instance being managed.
    
    Yields:
        None: Provides a context for the application's lifespan management.
    
    Side Effects:
        - Prints "lifespan" to indicate lifecycle management has started
        - Initializes the document converter using `init_converter()`
    """
    print("lifespan")
    await init_converter()
    yield

app = FastAPI(
    title="Minerva",
    version=version,
    license="MIT",
    lifespan=lifespan,
)

register_middleware(app)
app.include_router(upload_router, prefix=f"/api/{version}", tags=["file_upload"])
