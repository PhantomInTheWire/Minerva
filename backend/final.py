import os
import asyncio
import getpass
from datetime import datetime
from hashlib import md5
from typing import Dict, List
import pandas as pd
import seaborn as sns
import tiktoken
from langchain_community.graphs import Neo4jGraph
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from langchain_text_splitters import TokenTextSplitter
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import BaseOutputParser


os.environ["NEO4J_URI"] = "bolt://localhost:7687"
os.environ["NEO4J_USERNAME"] = "neo4j"
os.environ["NEO4J_PASSWORD"] = "your_password_here"


graph = Neo4jGraph(refresh_schema=False)

graph.query("CREATE CONSTRAINT IF NOT EXISTS FOR (c:Chunk) REQUIRE c.id IS UNIQUE")
graph.query("CREATE CONSTRAINT IF NOT EXISTS FOR (c:AtomicFact) REQUIRE c.id IS UNIQUE")
graph.query("CREATE CONSTRAINT IF NOT EXISTS FOR (c:KeyElement) REQUIRE c.id IS UNIQUE")
graph.query("CREATE CONSTRAINT IF NOT EXISTS FOR (d:Document) REQUIRE d.id IS UNIQUE")

os.environ["GOOGLE_API_KEY"]="AIzaSyASNOYxWqb_JI7TDXPZDIKt6S-uCJkj1sg"



with open('file.md', 'r') as f:
    text = f.read()

construction_system = """
You are now an intelligent assistant tasked with meticulously extracting both key elements and
atomic facts from a long text. Your response MUST be in valid JSON format with the following structure:
{{
    "atomic_facts": [
        {{
            "key_elements": ["element1", "element2", ...],
            "atomic_fact": "A concise fact statement"
        }}
    ]
}}

Guidelines for extraction:
1. Key Elements: The essential nouns (e.g., characters, times, events, places, numbers), verbs (e.g.,
actions), and adjectives (e.g., states, feelings) that are pivotal to the text's narrative.
2. Atomic Facts: The smallest, indivisible facts, presented as concise sentences. These include
propositions, theories, existences, concepts, and implicit elements like logic, causality, event
sequences, interpersonal relationships, timelines, etc.

Requirements:
#####
1. Ensure that all identified key elements are reflected within the corresponding atomic facts.
2. Extract key elements and atomic facts comprehensively, especially those that are
important and potentially query-worthy and do not leave out details.
3. Replace pronouns with their specific noun counterparts (e.g., change I, He, She to actual names).
4. Present key elements and atomic facts in the same language as the original text.
5. IMPORTANT: Your response MUST be valid JSON that matches the structure shown above.
"""

construction_human = """Use the given format to extract information from the 
following input: {input}"""

construction_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            construction_system,
        ),
        (
            "human",
            (
                "Use the given format to extract information from the "
                "following input: {input}"
            ),
        ),
    ]
)

class AtomicFact(BaseModel):
    key_elements: List[str] = Field(description="""The essential nouns (e.g., characters, times, events, places, numbers), verbs (e.g.,
actions), and adjectives (e.g., states, feelings) that are pivotal to the atomic fact's narrative.""")
    atomic_fact: str = Field(description="""The smallest, indivisible facts, presented as concise sentences. These include
propositions, theories, existences, concepts, and implicit elements like logic, causality, event
sequences, interpersonal relationships, timelines, etc.""")

class Extraction(BaseModel):
    atomic_facts: List[AtomicFact] = Field(description="List of atomic facts")

model = GoogleGenerativeAI(model="gemini-2.0-flash-exp", temperature=0)
class CustomOutputParser(BaseOutputParser):
    def parse(self, text):
        try:
            import re
            import json
            text = text.replace('\\n', '\n').replace('\\"', '"')
            json_match = re.search(r'\{(?:[^{}]|\{[^{}]*\})*\}', text)
            if json_match:
                json_str = json_match.group()
                # Remove any potential trailing/leading whitespace
                json_str = json_str.strip()
                try:
                    parsed_json = json.loads(json_str)
                    # Ensure the output is in the correct format with atomic_facts array
                    if "atomic_facts" not in parsed_json:
                        if "key_elements" in parsed_json and "atomic_fact" in parsed_json:
                            # Single fact object - wrap it in atomic_facts array
                            parsed_json = {"atomic_facts": [parsed_json]}
                    return json.dumps(parsed_json)
                except json.JSONDecodeError as je:
                    # If JSON parsing fails, try to fix common issues
                    json_str = re.sub(r',\s*([}\]])', r'\1', json_str)
                    parsed_json = json.loads(json_str)
                    return json.dumps(parsed_json)
            else:
                facts = []
                current_elements = []
                current_fact = ""
                
                for line in text.split('\n'):
                    line = line.strip()
                    if line.startswith('*') and ':' not in line:
                        if current_elements and current_fact:
                            facts.append({
                                "key_elements": current_elements,
                                "atomic_fact": current_fact
                            })
                        current_fact = line.strip('* ')
                        current_elements = []
                    elif ':' in line:
                        elements = line.split(':')[1].strip()
                        current_elements.extend([e.strip(' *') for e in elements.split(',')])
                
                if current_elements and current_fact:
                    facts.append({
                        "key_elements": current_elements,
                        "atomic_fact": current_fact
                    })
                
                result = {"atomic_facts": facts}
                return json.dumps(result)
        except Exception as e:
            raise ValueError(f"Failed to parse output: {str(e)}")

    def get_format_instructions(self):
        return ""

custom_parser = CustomOutputParser()
parser = PydanticOutputParser(pydantic_object=Extraction)
construction_chain = construction_prompt | model | custom_parser | parser

def encode_md5(text):
    return md5(text.encode("utf-8")).hexdigest()

import_query = """
MERGE (d:Document {id:$document_name})
WITH d
UNWIND $data AS row
MERGE (c:Chunk {id: row.chunk_id})
SET c.text = row.chunk_text,
    c.index = row.index,
    c.document_name = row.document_name
MERGE (d)-[:HAS_CHUNK]->(c)
WITH c, row
UNWIND row.atomic_facts AS af
MERGE (a:AtomicFact {id: af.id})
SET a.text = af.atomic_fact
MERGE (c)-[:HAS_ATOMIC_FACT]->(a)
WITH c, a, af
UNWIND af.key_elements AS ke
MERGE (k:KeyElement {id: ke})
MERGE (a)-[:HAS_KEY_ELEMENT]->(k)
"""

async def process_document(text, document_name, chunk_size=4000, chunk_overlap=200):
    start = datetime.now()
    print(f"Started extraction at: {start}")
    text_splitter = TokenTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    texts = text_splitter.split_text(text)
    print(f"Total text chunks: {len(texts)}")
    tasks = [
        asyncio.create_task(construction_chain.ainvoke({"input":chunk_text}))
        for index, chunk_text in enumerate(texts)
    ]
    results = await asyncio.gather(*tasks)
    print(f"Finished LLM extraction after: {datetime.now() - start}")
    docs = [el.model_dump() for el in results]
    for index, doc in enumerate(docs):
        doc['chunk_id'] = encode_md5(texts[index])
        doc['chunk_text'] = texts[index]
        doc['index'] = index
        for af in doc["atomic_facts"]:
            af["id"] = encode_md5(af["atomic_fact"])
    graph.query(import_query, 
            params={"data": docs, "document_name": document_name})
    graph.query("""MATCH (c:Chunk)<-[:HAS_CHUNK]-(d:Document)
WHERE d.id = $document_name
WITH c ORDER BY c.index WITH collect(c) AS nodes
UNWIND range(0, size(nodes) -2) AS index
WITH nodes[index] AS start, nodes[index + 1] AS end
MERGE (start)-[:NEXT]->(end)
""",
        params={"document_name":document_name})
    print(f"Finished import at: {datetime.now() - start}")

def num_tokens_from_string(string: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model("gpt-4")
    num_tokens = len(encoding.encode(string))
    return num_tokens

async def main():
    await process_document(text, text[:10], chunk_size=1000, chunk_overlap=200)

if __name__ == "__main__":
    asyncio.run(main())
