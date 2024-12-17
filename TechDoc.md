# Minerva: Technical Design Document

## Overview
Minerva is an AI-driven learning platform designed to revolutionize the way individuals interact with educational materials.
It allows users to curate notebooks containing a wide variety of resources, including PDFs, markdown files, LaTeX documents, multimedia, and even YouTube links. These notebooks serve as the foundation for interaction with advanced AI agents capable of answering questions, generating quizzes, analyzing user performance, and recommending tailored learning paths. Users can also explore visual tools like mind maps and learning roadmaps to better understand and retain complex topics.

## Features
### Core Features
1. **Notebook Creation and Management**
   - Users can create and organize notebooks, uploading and managing a variety of materials such as:
     - PDF files
     - Markdown/text/LaTeX/Source Code files
     - YouTube video links
     - Raw MP4/MP3 files
     - .docx, .pptx
     - .zip for bundled files
   - The system categorizes materials by topic, storing them in a PostgreSQL database for efficient retrieval.

2. **AI Agent Interaction**
   - Users interact with an AI **agents** capable of:
     - Querying the database to answer questions based on the user's materials.
     - Generating quizzes tailored to the user's knowledge and tracking performance.
     - Recommending areas of improvement and creating personalized learning roadmaps.
     - Crafting custom video lectures and generating flashcards for specific topics.
     - Providing answers to general subject-related queries.
     - Web search agent using serper api that can search the web just in case context is too limited to answer the users queries

3. **Notebook Sharing**
   - Enable seamless sharing of notebooks with other users to foster collaboration and collective learning.

4. **Visualization Tools**
   - Create dynamic mind maps and learning roadmaps with the help of:
     - **Mermaid.js** for interactive visualizations.
     - **PlantUML** for detailed diagrams.

5. **Spaced Repetition for Flashcards**
   - Boost memorization efficiency by implementing AI-optimized intervals for flashcard reviews.
## Architecture
### System Architecture
The application comprises several components that work together to provide an intelligent and interactive learning experience:

- **Frontend**: ReactJS and NextJS
- **Backend**: FastAPI+rust crates for performance intensive video and data processing tasks
- **Database**: PostgreSQL for storing categorized learning materials
- **AI/ML Framework**: combination of different llms including but limited to gemini-2.0-flash, gemini-1.5-pro, llama3.3(groq) depending on speed and task complexity
- **Visualization Tools**: Integration of Mermaid.js and PlantUML for rendering visual elements.

### High-Level Workflow
1. **Data Ingestion**
   - Users upload learning materials, which are categorized and stored in the PostgreSQL database.

2. **AI Interaction**
   - **Agent 1**: Acts as the orchestrator, analyzing user queries to determine relevant data from the database. It identifies the task type and delegates it to the appropriate specialized agent.
   - **Specialized Agents**:
     - **Question Answering Agent**: Provides concise and relevant responses to user queries.
     - **Quiz Generation Agent**: Designs customized quizzes based on user materials.
     - **Slide/Video Generation Agent**: Generates slides or video lectures tailored to specific topics.
     - **Flashcard Creation Agent**: Produces flashcards optimized for memorization.
     - **Roadmap/Mindmap Agent**: Creates personalized learning roadmaps and visually appealing mind maps.
     - **Research Agent**: An agent that can access the internet, any of the other agents can call this if they find their context lacking and ask for direction.

3. **Collaboration and Sharing**
   - Shared notebooks enable multiple users to contribute and collaborate effectively.

4. **Visualization**
   - Mind maps and roadmaps are dynamically generated using Mermaid.js and PlantUML, providing a clear overview of topics and their relationships.

## Technology Stack
### Frontend
- **Framework**: React/Nextjs, rive
- **Languages**: typescript, tailwindcss

### Backend
- **Framework**: fastapi, actix(just in case)
- **Languages**: python3.x, rust

### Database
- **Type**: Relational Database
- **Technology**: PostgreSQL
### Visualization
- **Mermaid.js**: For interactive and dynamic mind maps.
- **PlantUML**: For generating detailed visual roadmaps and diagrams.
## Development Plan
### Phase 1: Core Functionality
1. Build the notebook creation and material categorization system.
2. Set up PostgreSQL database to store and manage user materials.
3. Develop AI agent functionality for querying and basic question answering.
4. Basic UI and Simple Animations

### Phase 2: Advanced Features
1. Implement quiz generation and performance analysis.
2. Implement slide and video generation.
3. Develop visualization tools using Mermaid.js and PlantUML.
4. Crazy smooth and slick Animations

### Phase 3: Enhancements
1. Internet access agent
2. Add collaboration features for sharing notebooks.
3. maybe mobile or native desktop apps

## Roles and Responsibilities(tbd)

### Glossary
- **Notebook**: A digital collection of user-uploaded materials categorized by topic.
- **AI Agent**: An intelligent system that assists users by performing various tasks such as answering questions, creating quizzes, and generating personalized content.
- Serper: Best Google search api
- Groq: very fast and free llama3.3 endpoint based on LPUs
- LPU: fancy chips that run models very fast

## References
https://github.com/ishu-codes/vedanta/
https://github.com/codebyyashvi/SIH
https://github.com/S0L009/COMIC-IFY_OneAPI
https://github.com/kiriland/YHack2024
https://devpost.com/software/chatedu-0k4dgx
https://github.com/suno-ai/bark.git
