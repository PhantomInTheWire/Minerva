from neo4j import GraphDatabase
from ..middleware import logger
from ..error import KnowledgeGraphError
from .db_manager import Neo4jConnectionManager

class KnowledgeGraphRepository:
    def __init__(self):
        self.db_manager = Neo4jConnectionManager()

    def get_entire_graph(self):
        """Retrieve the entire knowledge graph from Neo4j."""
        try:
            driver = self.db_manager.get_driver()
            with driver.session() as session:
                nodes_result = session.run("""
                    MATCH (n)
                    RETURN collect({
                        id: id(n),
                        labels: labels(n),
                        properties: properties(n)
                    }) as nodes
                """)
                nodes = nodes_result.single()["nodes"]

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

            return {
                "nodes": nodes,
                "relationships": relationships
            }

        except Exception as e:
            logger.error(f"Error fetching knowledge graph: {str(e)}")
            raise KnowledgeGraphError(f"Failed to fetch knowledge graph", {"error": str(e)})