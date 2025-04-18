from itext2kg import iText2KG
from itext2kg.graph_integration import GraphIntegrator
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from ..middleware import logger
from ..error import KnowledgeGraphError
from .repository import KnowledgeGraphRepository
from .db_manager import Neo4jConnectionManager

class GraphCreationService:
    def __init__(self):
        self.repository = KnowledgeGraphRepository()
        self.db_manager = Neo4jConnectionManager() # Create an instance of Neo4jConnectionManager

    async def create_knowledge_graph(self, markdown_string: str) -> dict:
        """Process markdown and create knowledge graph in Neo4j."""
        if not markdown_string:
            raise KnowledgeGraphError("Empty markdown string provided")

        logger.info("Starting markdown processing...")
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash-8b",
            temperature=0.7
        )
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004"
        )
        logger.info("LLM and Embedding Models initialized.")

        itext2kg = iText2KG(llm_model=llm, embeddings_model=embeddings)
        logger.info("iText2KG initialized.")

        try:
            cleaned_markdown = markdown_string.strip()
            if '{' in cleaned_markdown or '}' in cleaned_markdown:
                cleaned_markdown = cleaned_markdown.replace('{', '{{').replace('}', '}}')

            try:
                kg = itext2kg.build_graph(sections=[cleaned_markdown])
                logger.info("Knowledge Graph built.")
            except ValueError as ve:
                logger.error(f"Validation error while building graph: {str(ve)}")
                raise KnowledgeGraphError(f"Invalid markdown format", {"error": str(ve)})
        except Exception as e:
            logger.error(f"Error building knowledge graph: {str(e)}")
            raise KnowledgeGraphError(f"Failed to build knowledge graph", {"error": str(e)})

        graph_integrator = GraphIntegrator(
            uri=self.db_manager.neo4j_url,
            username=self.db_manager.neo4j_user,
            password=self.db_manager.neo4j_password
        )
        logger.info("Visualizing and integrating Knowledge Graph into Neo4j...")
        graph_integrator.visualize_graph(knowledge_graph=kg)
        logger.info("Knowledge Graph visualized and integrated into Neo4j.")
        logger.info("Process Complete.")
        return {"status": "success", "message": "Knowledge graph created and integrated into Neo4j"}
