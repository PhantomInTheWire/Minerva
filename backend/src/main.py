from contextlib import asynccontextmanager
from fastapi import FastAPI
from .fileupload.router import upload_router
from .knowledge_graphs.router import knowledge_graph_router
from .middleware import register_middleware
from .converter import init_converter
from .newGraph.router import newGraph

version="v1"

@asynccontextmanager
async def lifespan(app: FastAPI):
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
app.include_router(knowledge_graph_router, prefix=f"/api/{version}", tags=["knowledge_graph"])
app.include_router(newGraph, prefix=f"/api/{version}", tags=["new"])