from fastapi import APIRouter, Body
from .service import KnowledgeGraphService
from ..middleware import logger
from ..error import handle_api_errors

knowledge_graph_router = APIRouter()

@knowledge_graph_router.get("/knowledge-graph")
@handle_api_errors
async def markdown_to_neo4j_kg(markdown_string: str):
    """
    Processes a markdown string, extracts knowledge using iText2KG, and adds it to a local Neo4j graph database.

    Args:
        markdown_string: The markdown content to process, sent in request body.

    Returns:
        dict: Status and message indicating success or failure.
    """
    service = KnowledgeGraphService()
    logger.success(await service.create_knowledge_graph(markdown_string))
    return {"status": "success", "message": "Knowledge graph created and integrated into Neo4j"}

@knowledge_graph_router.get("/graph")
@handle_api_errors
async def get_graph():
    """Retrieves the entire knowledge graph from Neo4j database.

    Returns:
        dict: Contains nodes and relationships of the graph.
    """
    service = KnowledgeGraphService()
    return await service.get_entire_graph()