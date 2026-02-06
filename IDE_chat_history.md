Prompt: /speckit.constitution Create a Constitution for Project Chimera. Core principles: 1) Spec-Driven Development is law; no code without a spec. 2) Safety First; every live post must pass the Symbolic Guardian and Human-in-the-Loop gate. 3) Agentic Traceability; all AI-generated code must explain its alignment with specs/technical.md. 4) Standardized Communication; all agents must use MCP primitives and standardized I/O contracts.

2. Define the "What" and "Why"
Prompt: /speckit.specify Specify the 'Autonomous Influencer Factory.' The goal is a system where a Hierarchical Swarm identifies trends, generates video content, and submits it for safety review. Key users: The Human-in-the-Loop (Governor) and the AI Agent Swarm (Workers). Requirements: Autonomous trend discovery, automated video drafting, and a 'Symbolic Guardian' layer to prevent brand damage or prompt injection.

3. Architect the Solution
Prompt: /speckit.plan Plan the technical architecture for Chimera.

Pattern: Hierarchical Swarm (Planner -> Workers -> Judge).

Stack: Python (uv for deps), Docker for containerization, GitHub Actions for CI/CD.

Data Layer: Hybrid SQL (PostgreSQL for Identity) + NoSQL (MongoDB for Video Metadata) + Vector DB (Pinecone for Memory).

Integrations: Coinbase AgentKit for economic agency, YouTube/TikTok APIs for delivery.

Security: A 'Symbolic Guardian' safety layer that validates content against hardcoded rules before requesting human approval.

4. Break Down the Implementation
Prompt: /speckit.tasks Generate a task list based on the implementation plan. Focus on:

Setting up the specs/ directory with _meta.md, functional.md, and technical.md.

Initializing the skills/ directory with README contracts for fetch_trends, generate_script, and symbolic_judge.

Creating the tests/ suite with failing TDD tests for the skills and data schema.

Configuring the Dockerfile, Makefile, and GitHub Actions workflow for automated governance.

5. Execute the Infrastructure Build
Prompt: /speckit.implement Implement the project infrastructure. Focus on the structural skeleton: create the directory hierarchy, the pyproject.toml, the Makefile with setup and test commands, and the initial failing test files. Do not implement the full logic for the skills yet; only build the 'empty slots' and the CI/CD pipeline that proves the system is ready for agentic development.