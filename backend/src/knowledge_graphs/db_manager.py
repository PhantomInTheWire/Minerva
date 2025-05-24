from neo4j import GraphDatabase
from ..config import Settings
from ..middleware import logger
from ..error import KnowledgeGraphError

class Neo4jConnectionManager:
    def __init__(self):
        """
        Initializes the Neo4jConnectionManager with connection parameters from the configuration.
        
        Loads the Neo4j URL, username, and password from the Settings object and prepares the internal driver attribute for future connection management.
        """
        self.neo4j_url = Settings.NEO4J_URL
        self.neo4j_user = Settings.NEO4J_USER
        self.neo4j_password = Settings.NEO4J_PASSWORD
        self._driver = None

    def get_driver(self):
        """
        Returns the Neo4j driver instance, initializing it if necessary.
        
        If the driver cannot be created, raises a KnowledgeGraphError with details about the failure.
        """
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
        """
        Closes the Neo4j driver connection and resets the internal driver state.
        
        If a driver connection exists, it is closed and the internal reference is cleared.
        """
        if self._driver:
            self._driver.close()
            self._driver = None