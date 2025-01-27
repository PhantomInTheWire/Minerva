from fastapi import APIRouter

knowledge_graph_router = APIRouter()

from itext2kg import iText2KG
from itext2kg.graph_integration import GraphIntegrator
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from ..middleware import logger
from ..config import Settings

@knowledge_graph_router.get("/knowledge-graph")
def markdown_to_neo4j_kg(markdown_string: str):
    """
    Processes a markdown string, extracts knowledge using iText2KG, and adds it to a local Neo4j graph database.

    Args:
        markdown_string: The large markdown string to process.

    Returns:
        None.  The function visualizes the graph in Neo4j.
    """

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

    kg = itext2kg.build_graph(sections=[markdown_string])
    logger.info("Knowledge Graph built.")

    graph_integrator = GraphIntegrator(uri=Settings.NEO4J_URL, username=Settings.NEO4J_USER, password=Settings.NEO4J_PASSWORD)
    logger.info("Visualizing and integrating Knowledge Graph into Neo4j...")
    graph_integrator.visualize_graph(knowledge_graph=kg)
    logger.info("Knowledge Graph visualized and integrated into Neo4j.")
    logger.info("Process Complete.")
    return {"knowledge_graph": "done"}
