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
