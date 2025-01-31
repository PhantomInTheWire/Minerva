import os
from pathlib import Path
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings as GoogleGeminiEmbeddings
from langchain_community.vectorstores import Neo4jVector
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.chains import RetrievalQA
from langchain_community.graphs import Neo4jGraph

# 1. Set up Google Gemini API
def setup_ggai_llm():
    return GoogleGenerativeAI(
        google_api_key=os.environ["GOOGLE_API_KEY"],
        model="gemini-2.0-flash-exp",
        temperature=0.2
    )

# 2. Set up Neo4j connection
def setup_neo4j():
    return Neo4jGraph(
        url="neo4j://localhost:7687",
        username="neo4j",
        password="your_password_here",
        database="neo4j"
    )

# 3. Define LLMs and embeddings
neo4j_graph = setup_neo4j()
embeddings = GoogleGeminiEmbeddings(
    google_api_key=os.environ["GOOGLE_API_KEY"],
    model="models/embedding-001"
)

# 4. Create Neo4j vector index if it doesn't exist
def create_vector_index_if_not_exists():
    # Check if index exists
    existing_indexes = neo4j_graph.query(
        "SHOW INDEXES YIELD name, type WHERE type = 'VECTOR' AND name = 'pages'"
    )
    if not existing_indexes:  # If no matching index found
        neo4j_graph.query(
            "CALL db.index.vector.createNodeIndex('pages', 'Page', 'embeddings', 768, 'cosine')"
        )
        print("Vector index 'pages' created successfully.")
    else:
        print("Vector index 'pages' already exists.")

create_vector_index_if_not_exists()

# 5. Set up RetrievalQA with Neo4j integration
retriever = Neo4jVector.from_existing_index(
    embedding=embeddings,
    url="neo4j://localhost:7687",
    username="neo4j",
    password="your_password_here",
    index_name="pages",
)

compression_llm = GoogleGenerativeAI(model="gemini-pro", temperature=0)
compression_chain = LLMChainExtractor.from_llm(compression_llm)

compressor = ContextualCompressionRetriever(
    base_compressor=compression_chain,
    base_retriever=retriever,
)

llm = setup_ggai_llm()

qa = RetrievalQA.from_llm(
    llm=llm,
    retriever=compressor,
    return_source_documents=False,
)

# 6. Run query
def run_query(query):
    result = qa.run(query)
    print(f"Answer: {result}")

# Example usage
run_query("What's the process to build an application on the Neo4j platform?")