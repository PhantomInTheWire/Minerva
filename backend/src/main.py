from contextlib import asynccontextmanager
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from fastapi import FastAPI
from .fileupload.router import upload_router
from .middleware import register_middleware

version="v1"
app = FastAPI(
    title="Minerva",
    version=version,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code: Initialize resources here
    converter = PdfConverter(artifact_dict=create_model_dict())
    yield

register_middleware(app)
app.include_router(upload_router, prefix=f"/api/{version}", tags=["file", "upload"])
