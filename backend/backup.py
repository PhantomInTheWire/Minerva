import os
from neo4j import GraphDatabase
import psycopg2
from datetime import datetime
import json
import hashlib


class Neo4jToPostgresBackup:
    def __init__(self, neo4j_uri, neo4j_user, neo4j_password,
                 pg_host, pg_database, pg_user, pg_password, pg_port=5432):
        """
                 Initializes connections to Neo4j and PostgreSQL databases for backup operations.
                 
                 Establishes a Neo4j driver and a PostgreSQL connection with an active cursor using the provided connection parameters.
                 """
                 self.neo4j_driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
        self.pg_conn = psycopg2.connect(
            host=pg_host,
            database=pg_database,
            user=pg_user,
            password=pg_password,
            port=pg_port
        )
        self.pg_cursor = self.pg_conn.cursor()

    def setup_postgres_schema(self):
        """
        Creates a normalized (3NF) schema in PostgreSQL for backing up Neo4j data.
        
        Drops existing backup-related tables if they exist, then creates tables for node types, relationship types, nodes, node-type mappings, property keys, node properties, relationships, and relationship properties, establishing appropriate primary and foreign key constraints. Commits the schema changes to the database.
        """
        # Drop existing tables if they exist (in correct order)
        drop_tables = [
            "DROP TABLE IF EXISTS relationship_properties CASCADE",
            "DROP TABLE IF EXISTS node_properties CASCADE",
            "DROP TABLE IF EXISTS node_type_mappings CASCADE",
            "DROP TABLE IF EXISTS relationships CASCADE",
            "DROP TABLE IF EXISTS nodes CASCADE",
            "DROP TABLE IF EXISTS node_types CASCADE",
            "DROP TABLE IF EXISTS relationship_types CASCADE",
            "DROP TABLE IF EXISTS property_keys CASCADE"
        ]

        for drop_table in drop_tables:
            self.pg_cursor.execute(drop_table)

        # Create tables in correct order
        tables = [
            """
            CREATE TABLE IF NOT EXISTS node_types (
                type_id SERIAL PRIMARY KEY,
                label TEXT UNIQUE NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS relationship_types (
                type_id SERIAL PRIMARY KEY,
                type_name TEXT UNIQUE NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS nodes (
                node_id TEXT PRIMARY KEY,
                backup_timestamp TIMESTAMP NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS node_type_mappings (
                node_id TEXT REFERENCES nodes(node_id),
                type_id INTEGER REFERENCES node_types(type_id),
                PRIMARY KEY (node_id, type_id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS property_keys (
                key_id SERIAL PRIMARY KEY,
                key_name TEXT UNIQUE NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS node_properties (
                node_id TEXT REFERENCES nodes(node_id),
                key_id INTEGER REFERENCES property_keys(key_id),
                property_value TEXT,
                PRIMARY KEY (node_id, key_id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS relationships (
                relationship_id TEXT PRIMARY KEY,
                start_node_id TEXT REFERENCES nodes(node_id),
                end_node_id TEXT REFERENCES nodes(node_id),
                relationship_type_id INTEGER REFERENCES relationship_types(type_id),
                backup_timestamp TIMESTAMP NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS relationship_properties (
                relationship_id TEXT REFERENCES relationships(relationship_id),
                key_id INTEGER REFERENCES property_keys(key_id),
                property_value TEXT,
                PRIMARY KEY (relationship_id, key_id)
            )
            """
        ]

        for table in tables:
            self.pg_cursor.execute(table)

        self.pg_conn.commit()

    def get_or_create_type_id(self, type_name, type_table, name_column):
        """
        Retrieves the ID for a given type from the specified table, inserting it if it does not exist.
        
        Args:
            type_name: The name of the type to look up or insert.
            type_table: The table in which to search or insert the type.
            name_column: The column name representing the type's name.
        
        Returns:
            The unique ID of the type from the specified table.
        """
        self.pg_cursor.execute(f"""
            INSERT INTO {type_table} ({name_column})
            VALUES (%s)
            ON CONFLICT ({name_column}) DO UPDATE
            SET {name_column} = EXCLUDED.{name_column}
            RETURNING type_id
        """, (type_name,))
        return self.pg_cursor.fetchone()[0]

    def get_or_create_property_key_id(self, key_name):
        """
        Retrieves the ID of a property key from the database, inserting it if it does not exist.
        
        Args:
            key_name: The name of the property key to retrieve or create.
        
        Returns:
            The unique ID of the property key.
        """
        self.pg_cursor.execute("""
            INSERT INTO property_keys (key_name)
            VALUES (%s)
            ON CONFLICT (key_name) DO UPDATE
            SET key_name = EXCLUDED.key_name
            RETURNING key_id
        """, (key_name,))
        return self.pg_cursor.fetchone()[0]

    def backup_nodes(self):
        """
        Backs up all nodes from the Neo4j database into the normalized PostgreSQL schema.
        
        For each node, inserts or updates its record in the `nodes` table with a backup timestamp, maps its labels to type IDs in `node_types` and records these in `node_type_mappings`, and stores all properties in `node_properties`. Commits all changes after processing.
        """
        with self.neo4j_driver.session() as session:
            query = """
                MATCH (n)
                RETURN id(n) as node_id, labels(n) as labels, properties(n) as properties
            """

            current_time = datetime.now()
            result = session.run(query)

            for record in result:
                node_id = str(record["node_id"])

                # Insert node
                self.pg_cursor.execute("""
                    INSERT INTO nodes (node_id, backup_timestamp)
                    VALUES (%s, %s)
                    ON CONFLICT (node_id) DO UPDATE
                    SET backup_timestamp = EXCLUDED.backup_timestamp
                """, (node_id, current_time))

                # Handle labels
                for label in record["labels"]:
                    type_id = self.get_or_create_type_id(label, "node_types", "label")
                    self.pg_cursor.execute("""
                        INSERT INTO node_type_mappings (node_id, type_id)
                        VALUES (%s, %s)
                        ON CONFLICT DO NOTHING
                    """, (node_id, type_id))

                # Handle properties
                properties = dict(record["properties"])
                for key, value in properties.items():
                    key_id = self.get_or_create_property_key_id(key)
                    self.pg_cursor.execute("""
                        INSERT INTO node_properties (node_id, key_id, property_value)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (node_id, key_id) DO UPDATE
                        SET property_value = EXCLUDED.property_value
                    """, (node_id, key_id, str(value)))

            self.pg_conn.commit()

    def backup_relationships(self):
        """
        Backs up all relationships from Neo4j into the PostgreSQL schema in 3NF format.
        
        Extracts all relationships from the Neo4j database, including their IDs, types, start and end nodes, and properties. Each relationship and its properties are inserted or updated in the corresponding PostgreSQL tables, ensuring type and property key references are maintained. Commits all changes after processing.
        """
        with self.neo4j_driver.session() as session:
            query = """
                MATCH ()-[r]->()
                RETURN id(r) as rel_id, 
                       id(startNode(r)) as start_node_id,
                       id(endNode(r)) as end_node_id,
                       type(r) as rel_type,
                       properties(r) as properties
            """

            current_time = datetime.now()
            result = session.run(query)

            for record in result:
                rel_id = str(record["rel_id"])
                relationship_type_id = self.get_or_create_type_id(record["rel_type"], "relationship_types", "type_name")

                # Insert relationship
                self.pg_cursor.execute("""
                    INSERT INTO relationships 
                    (relationship_id, start_node_id, end_node_id, relationship_type_id, backup_timestamp)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (relationship_id) DO UPDATE
                    SET start_node_id = EXCLUDED.start_node_id,
                        end_node_id = EXCLUDED.end_node_id,
                        relationship_type_id = EXCLUDED.relationship_type_id,
                        backup_timestamp = EXCLUDED.backup_timestamp
                """, (
                    rel_id,
                    str(record["start_node_id"]),
                    str(record["end_node_id"]),
                    relationship_type_id,
                    current_time
                ))

                # Handle properties
                properties = dict(record["properties"])
                for key, value in properties.items():
                    key_id = self.get_or_create_property_key_id(key)
                    self.pg_cursor.execute("""
                        INSERT INTO relationship_properties (relationship_id, key_id, property_value)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (relationship_id, key_id) DO UPDATE
                        SET property_value = EXCLUDED.property_value
                    """, (rel_id, key_id, str(value)))

            self.pg_conn.commit()

    def perform_backup(self):
        """
        Performs a full backup from Neo4j to PostgreSQL using a normalized schema.
        
        This method sets up the PostgreSQL schema, transfers all nodes and relationships from the Neo4j database, and ensures proper cleanup of resources. If an error occurs during the process, the PostgreSQL transaction is rolled back.
        """
        try:
            print("Setting up PostgreSQL schema...")
            self.setup_postgres_schema()

            print("Backing up nodes...")
            self.backup_nodes()

            print("Backing up relationships...")
            self.backup_relationships()

            print("Backup completed successfully!")

        except Exception as e:
            print(f"Error during backup: {str(e)}")
            self.pg_conn.rollback()
        finally:
            self.cleanup()

    def cleanup(self):
        """
        Closes all open connections to PostgreSQL and Neo4j.
        """
        self.pg_cursor.close()
        self.pg_conn.close()
        self.neo4j_driver.close()


if __name__ == "__main__":
    # Configuration
    neo4j_config = {
        "uri": "neo4j://localhost:7687",
        "user": "neo4j",
        "password": "your_password_here"
    }

    postgres_config = {
        "host": "localhost",
        "database": "minerva",
        "user": "postgres",
        "password": "your_password",
        "port": 5432
    }

    # Initialize and run backup
    backup = Neo4jToPostgresBackup(
        neo4j_uri=neo4j_config["uri"],
        neo4j_user=neo4j_config["user"],
        neo4j_password=neo4j_config["password"],
        pg_host=postgres_config["host"],
        pg_database=postgres_config["database"],
        pg_user=postgres_config["user"],
        pg_password=postgres_config["password"],
        pg_port=postgres_config["port"]
    )

    backup.perform_backup()