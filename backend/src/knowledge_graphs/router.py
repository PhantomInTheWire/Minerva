from fastapi import APIRouter

knowledge_graph_router = APIRouter()

from itext2kg import iText2KG
from itext2kg.graph_integration import GraphIntegrator
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from ..middleware import logger
from ..config import Settings
from neo4j import GraphDatabase

@knowledge_graph_router.get("/knowledge-graph")
async def markdown_to_neo4j_kg(markdown_string: str):
    """
    Processes a markdown string, extracts knowledge using iText2KG, and adds it to a local Neo4j graph database.

    Args:
        markdown_string: The large markdown string to process.

    Returns:
        dict: Status and message indicating success or failure.
    """
    if not markdown_string:
        return {"status": "error", "message": "Empty markdown string provided"}

    logger.info("Starting markdown processing...")
    openai_llm_model = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        temperature=0.7
    )
    openai_embeddings_model = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001"
    )
    logger.info("LLM and Embedding Models initialized.")

    itext2kg = iText2KG(llm_model=openai_llm_model, embeddings_model=openai_embeddings_model)

    logger.info("iText2KG initialized.")

    try:
        # Clean and validate markdown string
        cleaned_markdown = markdown_string.strip()
        if '{' in cleaned_markdown or '}' in cleaned_markdown:
            cleaned_markdown = cleaned_markdown.replace('{', '{{').replace('}', '}}')
            
        # Build knowledge graph with validated markdown
        try:
            kg = itext2kg.build_graph(sections=[cleaned_markdown])
            logger.info("Knowledge Graph built.")
        except ValueError as ve:
            logger.error(f"Validation error while building graph: {str(ve)}")
            return {"status": "error", "message": f"Invalid markdown format: {str(ve)}"}
    except Exception as e:
        logger.error(f"Error building knowledge graph: {str(e)}")
        return {"status": "error", "message": f"Failed to build knowledge graph: {str(e)}"}

    graph_integrator = GraphIntegrator(uri=Settings.NEO4J_URL, username=Settings.NEO4J_USER, password=Settings.NEO4J_PASSWORD)
    logger.info("Visualizing and integrating Knowledge Graph into Neo4j...")
    graph_integrator.visualize_graph(knowledge_graph=kg)
    logger.info("Knowledge Graph visualized and integrated into Neo4j.")
    logger.info("Process Complete.")
    return {"status": "success", "message": "Knowledge graph created and integrated into Neo4j"}

@knowledge_graph_router.get("/graph")
async def get_graph():
    """Retrieves the entire knowledge graph from Neo4j database.

    Returns:
        dict: Contains nodes and relationships of the graph.
    """
    logger.info("Fetching knowledge graph from Neo4j...")
    try:
        driver = GraphDatabase.driver(
            Settings.NEO4J_URL,
            auth=(Settings.NEO4J_USER, Settings.NEO4J_PASSWORD)
        )

        with driver.session() as session:
            # Query to get all nodes
            nodes_result = session.run("""
                MATCH (n)
                RETURN collect({
                    id: id(n),
                    labels: labels(n),
                    properties: properties(n)
                }) as nodes
            """)
            nodes = nodes_result.single()["nodes"]

            # Query to get all relationships
            rels_result = session.run("""
                MATCH ()-[r]->() 
                RETURN collect({
                    id: id(r),
                    type: type(r),
                    properties: properties(r),
                    source: id(startNode(r)),
                    target: id(endNode(r))
                }) as relationships
            """)
            relationships = rels_result.single()["relationships"]

        driver.close()
        logger.info("Successfully retrieved knowledge graph from Neo4j")
        return {
            "status": "success",
            "data": {
                "nodes": nodes,
                "relationships": relationships
            }
        }

    except Exception as e:
        logger.error(f"Error fetching knowledge graph: {str(e)}")
        return {"status": "error", "message": f"Failed to fetch knowledge graph: {str(e)}"}
