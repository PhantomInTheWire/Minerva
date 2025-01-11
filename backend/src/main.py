from fastapi import FastAPI
from .fileupload.router import upload_router
from .middleware import register_middleware

version="v1"
app = FastAPI(
    title="Minerva",
    version=version,
)
register_middleware(app)
app.include_router(upload_router, prefix=f"/api/{version}", tags=["file", "upload"])
