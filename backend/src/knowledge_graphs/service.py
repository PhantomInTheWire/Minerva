from ..middleware import logger
from .graph_creation_service import GraphCreationService
from .repository import KnowledgeGraphRepository

class KnowledgeGraphService:
    def __init__(self):
        self.graph_creation_service = GraphCreationService()
        self.repository = KnowledgeGraphRepository()

    async def create_knowledge_graph(self, markdown_string: str) -> dict:
        """Process markdown and create knowledge graph in Neo4j."""
        return await self.graph_creation_service.create_knowledge_graph(markdown_string)

    async def get_entire_graph(self) -> dict:
        """Retrieve the entire knowledge graph from Neo4j."""
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