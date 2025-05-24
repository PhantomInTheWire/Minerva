from ..middleware import logger
from .graph_creation_service import GraphCreationService
from .repository import KnowledgeGraphRepository

class KnowledgeGraphService:
    def __init__(self):
        """
        Initializes the KnowledgeGraphService with graph creation and repository components.
        """
        self.graph_creation_service = GraphCreationService()
        self.repository = KnowledgeGraphRepository()

    async def create_knowledge_graph(self, markdown_string: str) -> dict:
        """
        Creates a knowledge graph from a markdown string.
        
        Args:
            markdown_string: The markdown content to be processed into a knowledge graph.
        
        Returns:
            A dictionary representing the created knowledge graph.
        """
        return await self.graph_creation_service.create_knowledge_graph(markdown_string)

    async def get_entire_graph(self) -> dict:
        """
        Retrieves the complete knowledge graph from the repository.
        
        Returns:
            A dictionary containing the status and the retrieved graph data.
        
        Raises:
            Any exception encountered during retrieval is re-raised after logging.
        """
        logger.info("Fetching knowledge graph from Neo4j...")
        try:
            graph_data = self.repository.get_entire_graph()
            return {
                "status": "success",
                "data": graph_data
            }
        except Exception as e:
            logger.error(f"Error fetching knowledge graph: {str(e)}")
            raise