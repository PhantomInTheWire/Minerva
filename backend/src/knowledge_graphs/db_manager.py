from neo4j import GraphDatabase
from ..config import Settings
from ..middleware import logger
from ..error import KnowledgeGraphError

class Neo4jConnectionManager:
    def __init__(self):
        self.neo4j_url = Settings.NEO4J_URL
        self.neo4j_user = Settings.NEO4J_USER
        self.neo4j_password = Settings.NEO4J_PASSWORD
        self._driver = None

    def get_driver(self):
        if not self._driver:
            try:
                self._driver = GraphDatabase.driver(
                    self.neo4j_url,
                    auth=(self.neo4j_user, self.neo4j_password)
                )
            except Exception as e:
                logger.error(f"Failed to connect to Neo4j: {str(e)}")
                raise KnowledgeGraphError(f"Database connection failed", {"error": str(e)})
        return self._driver

    def close(self):
        if self._driver:
            self._driver.close()
            self._driver = None