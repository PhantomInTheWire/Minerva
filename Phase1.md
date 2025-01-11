# Phase 1

## Phase 1.00: Landing Page

1. Landing Page (7.5sp)
    - Intro (1sp)
        - Spline
    - Tut (2sp)
        - Macbook
        - Karan gif
    - Features (3sp)
        - Animated beam
        - Bentoo Grid
        - Multilingual Globe
    - Testimonial (1sp)
        - Infinite Moving Cards
    - Pricing (0.5sp)
        - Cards
--- 

## Phase 1.1: Basic Chat Infrastructure

1. Build the notebook creation and material categorization system.
    - Add better logging and middleware
    - set up db schemas and psql on docker
    - make it async!
    - set up alembic migrations
    - Basic Postgresql DB for storing notebooks and their materials(only pdf in this step)
2. Enable preprocessing methods to convert regular text into markdown semantically. 
    - Integrate ml pipelines to do this
3. Build the LightRAG/LazyGraphRag prototype using existing implementation
    - integrate existing graph rag approaches
    - try building something faster using light/lazy graph RAG
4. Set up PostgreSQL database to store and manage user materials.
    - Make sure it is easy to query and store
5. Develop AI agent functionality for querying and basic question answering using different RAG techniques.
    - Add an llm to query the RAG pipeline
6. Extend file upload to virtually any file type that can be converted to txt
    - more file type support
7. Integrate this functionality to a basic UI
8. Implement better preprocessing 
   - For files in pdf format (or pdf friendly formats like .docx or .pptx) add a different pre processing layer that semantically converts them into markdown and JSON for llm processing. find [here](https://www.youtube.com/watch?v=ueP-C_eTxTg) and more [here](https://youtu.be/_U14Rf2bEkk?si=V1ipHNkAXcOgsZ2j)
   - This will be useful for designing the next overview feature


---

## Phase 1.2: Sectional Overview

1. Develop Sectional Overview
   - Report Generation using Agentic RAG llamaindex (https://www.youtube.com/watch?v=3jnViQZKYHE)
   - Organize and optimize the markdown using smaller specialized models and make it look eye candy on the frontend.
   - Add sectional quizes and revision checkpoints etc to help track user progress.
   - The API for this would be GraphQL instead of REST since this is something that must be queried on demand as the contents being retrieved can be large, and the query responds with  nested JSON objects.
   - It should have a optional chat bot pop up on the right/left side bar that can take into context anything the user selects and doubts
