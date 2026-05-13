import re
from ..middleware import logger
from ..error import KnowledgeGraphError
from .db_manager import Neo4jConnectionManager

class GraphCreationService:
    def __init__(self):
        self.db_manager = Neo4jConnectionManager()

    async def create_knowledge_graph(self, markdown_string: str) -> dict:
        """Store markdown sections in Neo4j as a lightweight knowledge graph."""
        if not markdown_string:
            raise KnowledgeGraphError("Empty markdown string provided")

        try:
            cleaned_markdown = markdown_string.strip()
            sections = []
            current_title = "Document"
            current_body = []

            for line in cleaned_markdown.splitlines():
                heading = re.match(r"^(#{1,6})\s+(.*)$", line.strip())
                if heading:
                    if current_body or current_title != "Document":
                        sections.append({"title": current_title, "body": "\n".join(current_body).strip()})
                    current_title = heading.group(2).strip()
                    current_body = []
                else:
                    current_body.append(line)

            if current_body or current_title != "Document":
                sections.append({"title": current_title, "body": "\n".join(current_body).strip()})

            if not sections:
                sections = [{"title": "Document", "body": cleaned_markdown}]

            driver = self.db_manager.get_driver()
            with driver.session() as session:
                doc_result = session.run(
                    """
                    CREATE (d:MarkdownDocument {
                        content: $content,
                        section_count: $section_count,
                        created_at: datetime()
                    })
                    RETURN id(d) AS doc_id
                    """,
                    content=cleaned_markdown,
                    section_count=len(sections),
                )
                doc_id = doc_result.single()["doc_id"]

                session.run(
                    """
                    MATCH (d) WHERE id(d) = $doc_id
                    UNWIND range(0, size($sections) - 1) AS idx
                    WITH d, idx, $sections[idx] AS section
                    CREATE (s:MarkdownSection {
                        title: section.title,
                        body: section.body,
                        order: idx
                    })
                    CREATE (d)-[:HAS_SECTION]->(s)
                    """,
                    doc_id=doc_id,
                    sections=sections,
                )

            logger.info("Knowledge graph stored in Neo4j.")
            return {"status": "success", "message": "Knowledge graph created and integrated into Neo4j"}
        except Exception as e:
            logger.error(f"Error building knowledge graph: {str(e)}")
            raise KnowledgeGraphError(f"Failed to build knowledge graph", {"error": str(e)})
