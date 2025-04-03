# Archon Codebase Overview

## Project Definition

Archon is described as an "Agenteer" - an AI agent designed to autonomously build, refine, and optimize other AI agents. It serves both as a practical tool for developers and as an educational framework demonstrating the evolution of agentic systems.

## Project Evolution

The project has evolved through multiple versions:
- V1: Single agent implementation
- V2: Agentic workflow 
- V3: MCP (Model Context Protocol) support
- V4: Streamlit UI overhaul
- V5: Parallel specialized agents
- V6: Tool library and MCP integration (current version)

Each iteration builds upon the previous, with preserved versions in the `/iterations` directory.

## Core Architecture

### Main Components

1. **Agent Framework**
   - Built using Pydantic AI, LangGraph, and Supabase
   - Multi-agent architecture with specialized refiner agents

2. **Agent Graph System (`archon/archon_graph.py`)**
   - Manages the workflow between different agent components
   - Key functions:
     - `define_scope_with_reasoner`: Initial scoping of the agent to be created
     - `advisor_with_examples`: Component recommendation system
     - `coder_agent`: Creates the actual agent code
     - `refine_prompt`, `refine_tools`, `refine_agent`: Specialized refinement stages
     - `route_user_message`: Handles user interactions

3. **Pydantic AI Coder (`archon/pydantic_ai_coder.py`)**
   - Core implementation for code generation
   - Leverages the Pydantic AI framework
   - Uses AnthropicModel and OpenAIModel for LLM integration

4. **Agent Components**
   - `advisor_agent.py`: Recommends prebuilt tools and examples
   - `agent_prompts.py`: Contains prompt templates for all agents
   - `agent_tools.py`: Defines tools agents can use
   - `refiner_agents/`: Specialized agents for refining different aspects of created agents

5. **MCP Integration (`mcp/`)**
   - Model Context Protocol server implementation
   - Allows communication with external services
   - `/agent-resources/mcps/`: Contains configuration files for different MCP servers

6. **Tool Library (`agent-resources/`)**
   - Prebuilt tools for common agent tasks
   - Example agents that can be adapted
   - GitHub integration tools, web search tools, etc.

7. **User Interface (`streamlit_ui.py` and `streamlit_pages/`)**
   - Streamlit-based web interface
   - Multiple pages for different functionality:
     - `intro.py`: Landing page
     - `chat.py`: Interaction with the agent
     - `documentation.py`: Help and documentation
     - `environment.py`: Configuration settings
     - `mcp.py`: MCP server management
     - `database.py`: Database interaction
     - `agent_service.py`: Manages agent execution

## Key Features of Current Version (V6)

1. **Prebuilt Tools Library**: Collection of ready-to-use tools for common agent tasks
2. **Example Agents**: Reference implementations that can be adapted for new agents
3. **MCP Server Integrations**: Preconfigured connections to various external services
4. **Advisor Agent**: Recommends relevant prebuilt components based on requirements
5. **Enhanced Tools Refiner**: Validates and optimizes MCP server configurations
6. **Component Reuse**: Significantly reduces development time and hallucinations
7. **Multi-Agent Workflow**: Specialized refiner agents working together
8. **Streamlined External Access**: Easy integration with various services through MCP

## Workflow

1. **Initial Request**: User describes the AI agent they want to create
2. **Scope Definition**: Reasoner LLM creates a high-level scope for the agent
3. **Component Recommendation**: Advisor agent analyzes requirements and recommends relevant prebuilt components
4. **Prompt Creation**: Specialized agent creates prompt templates
5. **Tools Creation**: Specialized agent develops and optimizes tools
6. **Agent Code Generation**: Core agent creates the main code
7. **Final Refinement**: The complete agent is reviewed and optimized
8. **Deployment**: The completed agent is ready for use

## Technical Stack

- **Python**: Primary programming language
- **Pydantic AI**: Framework for creating structured agents
- **LangGraph**: Used for agent workflows and orchestration
- **Streamlit**: Web UI framework
- **Supabase**: Database and authentication
- **Docker**: Containerization for deployment
- **Various LLM APIs**: Integration with models like Claude (Anthropic) and GPT (OpenAI)
- **MCP**: Model Context Protocol for external service integration

## File Structure

- `/archon/`: Core agent implementation
- `/iterations/`: Historical versions of the project
- `/mcp/`: Model Context Protocol server
- `/streamlit_pages/`: UI components
- `/agent-resources/`: Prebuilt tools and examples
  - `/agent-resources/tools/`: Ready-to-use tools
  - `/agent-resources/examples/`: Example agent implementations
  - `/agent-resources/mcps/`: MCP server configurations
- `/utils/`: Utility functions and helpers
- `/public/`: Static assets

## Important Implementation Details

1. The core agent workflow is managed through LangGraph, which handles the transitions between different agent states.

2. The Pydantic AI framework provides strong typing and structure to the generated agents.

3. Agents communicate through a shared state object that gets passed between different components.

4. MCP servers follow a standard configuration approach, making it easy to add new integrations.

5. The streamlit UI provides a user-friendly interface for interacting with the system.

## Development Process

When exploring and extending the Archon codebase, consider:

1. Each iteration adds complexity but preserves the core functionality
2. The agent's workflow is modular and can be extended with new specialized agents
3. New tools can be added to the tool library for reuse across agents
4. MCP configurations follow a standard pattern that can be replicated for new services
5. The UI is component-based and can be extended with new pages

## Future Exploration Areas

1. Adding new specialized refiner agents for different aspects of agent creation
2. Extending the tool library with more prebuilt components
3. Adding new MCP server integrations for additional services
4. Enhancing the UI with more advanced visualization options
5. Exploring interoperability with other agent frameworks
