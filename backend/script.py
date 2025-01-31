from langchain_google_genai import GoogleGenerativeAI
from langchain_community.graphs import Neo4jGraph
from langchain.chains import GraphCypherQAChain
from langchain.prompts import PromptTemplate
import os

graph = Neo4jGraph(
    url="neo4j://localhost:7687",  
    username="neo4j",
    password="your_password_here",
    database="neo4j"
)

llm = GoogleGenerativeAI(model="gemini-2.0-flash-exp")

# Get schema information
schema_query = """
CALL db.labels() YIELD label
WITH collect(label) AS labels
CALL db.relationshipTypes() YIELD relationshipType
WITH labels, collect(relationshipType) AS relationships
RETURN {
    nodes: labels,
    relationships: relationships
} AS schema
"""
schema_info = graph.query(schema_query)

# Custom prompt for Cypher generation
CUSTOM_PROMPT = f"""
Given the question: {{question}}
Generate a Cypher query that uses basic pattern matching and relationships to return meaningful information. Exclude "embeddings" to avoid large responses.

Current Neo4j schema:
{schema_info}

Cypher query:
"""

chain = GraphCypherQAChain.from_llm(
    llm=llm,
    graph=graph,
    verbose=True,
    cypher_prompt=PromptTemplate(
        template=CUSTOM_PROMPT,
        input_variables=["question"]
    ),
    allow_dangerous_requests=True
)

def query_graph(question: str):
    try:
        result = chain.invoke({"question": question})
        return result['result']
    except Exception as e:
        return f"Error querying graph: {str(e)}"

from typing import List, Dict
import numpy as np
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate

def find_similar_concepts(input_dict: Dict) -> List[str]:
    concept_name = input_dict.get("concept_name") if isinstance(input_dict, dict) else input_dict
    threshold = input_dict.get("threshold", 0.85) if isinstance(input_dict, dict) else 0.85
    
    query = """
    MATCH (c1:Concept {name: $name}), (c2:Concept)
    WHERE c1.name <> c2.name
    WITH c1, c2,
         c1.embeddings AS embedding1,
         c2.embeddings AS embedding2
    RETURN c2.name,
           CASE
               WHEN embedding1 IS NOT NULL AND embedding2 IS NOT NULL
               THEN reduce(dot = 0.0, i IN range(0, size(split(embedding1, ','))-1) |
                    dot + toFloat(split(embedding1, ',')[i]) * toFloat(split(embedding2, ',')[i])) /
                    (sqrt(reduce(norm1 = 0.0, i IN range(0, size(split(embedding1, ','))-1) |
                        norm1 + toFloat(split(embedding1, ',')[i]) * toFloat(split(embedding1, ',')[i]))) *
                     sqrt(reduce(norm2 = 0.0, i IN range(0, size(split(embedding2, ','))-1) |
                        norm2 + toFloat(split(embedding2, ',')[i]) * toFloat(split(embedding2, ',')[i]))))
               ELSE 0
           END as similarity
    ORDER BY similarity DESC
    LIMIT 10
    """
    try:
        return graph.query(query, {"name": concept_name})
    except Exception as e:
        return f"Error finding similar concepts: {str(e)}"

tools = [
    Tool(
        name="Find Similar Concepts",
        func=find_similar_concepts,
        description="Find semantically similar concepts in the knowledge graph"
    ),
    Tool(
        name="Query Graph",
        func=query_graph,
        description="Query the knowledge graph using natural language"
    )
]

REACT_PROMPT = PromptTemplate(
    input_variables=["tools", "tool_names", "input", "agent_scratchpad"],
    template="""Answer the following questions as best you can using the following tools: {tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Question: {input}
{agent_scratchpad}"""
)

agent = create_react_agent(llm, tools, REACT_PROMPT)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

def process_query(query: str):
    """Process natural language queries using the agent."""
    try:
        return agent_executor.invoke({"input": query})
    except Exception as e:
        return f"Error processing query: {str(e)}"

if __name__ == "__main__":
    # print("\nQuerying about backend frameworks:")
    # print(query_graph("What are the main backend frameworks and their relationships?"))
    
    # print("\nQuerying about database connections:")
    # print(query_graph("How are databases typically connected in backend systems?"))
    
    # print("\nFinding concepts similar to 'API':")
    # print(find_similar_concepts("API"))
    
    # print("\nExploring backend architecture:")
    # print(query_graph("What are the key components of backend architecture and how are they related?"))
    
    print("\nProcessing complex query about graph reader:")
    print(process_query("What are services like graphreader and how is it different from graphrag and lighrag?"))
