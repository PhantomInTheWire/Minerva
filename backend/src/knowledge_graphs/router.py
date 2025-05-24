from fastapi import APIRouter, Body
from .service import KnowledgeGraphService
from ..middleware import logger
from ..error import handle_api_errors

knowledge_graph_router = APIRouter()

@knowledge_graph_router.get("/knowledge-graph")
@handle_api_errors
async def markdown_to_neo4j_kg(markdown_string: str):
    """
    Creates a knowledge graph from a markdown string and integrates it into a local Neo4j database.
    
    Args:
        markdown_string: Markdown content to be processed and converted into a knowledge graph.
    
    Returns:
        A dictionary with status and message indicating successful creation and integration of the knowledge graph.
    """
    service = KnowledgeGraphService()
    logger.success(await service.create_knowledge_graph(markdown_string))
    return {"status": "success", "message": "Knowledge graph created and integrated into Neo4j"}

@knowledge_graph_router.get("/graph")
@handle_api_errors
async def get_graph():
    """
    Retrieves the complete knowledge graph from the Neo4j database.
    
    Returns:
        dict: A dictionary containing all nodes and relationships in the graph.
    """
    service = KnowledgeGraphService()
    return await service.get_entire_graph()