# Archon Project Planning

## Project Overview

Archon is an "Agenteer" - an AI agent designed to autonomously build, refine, and optimize other AI agents. The project serves both as a practical tool for developers and as an educational framework demonstrating the evolution of agentic systems.

## Current Feature Development: Ollama and Google Gemini 2.5 Support

### Feature Request Goals

1. Add support for Ollama models (locally hosted open-source LLMs)
2. Add support for Google Gemini 2.5 API
3. Ensure these new models work with the existing agent architecture
4. Update the UI to allow selection of these model providers
5. Document the setup and configuration process
6. Implement performance benchmarking for model comparison
7. Add token budget management and cost estimation
8. Create fallback mechanisms between providers
9. Enhance security for API key management
10. Ensure cross-platform compatibility

### Technical Implementation Plan

#### A. Ollama Integration

1. Create a new module `archon/models/ollama.py` to implement Ollama API integration
2. Implement an `OllamaModel` class that conforms to the same interface as existing models
3. Update model selection logic to include Ollama models
4. Add configuration options to the environment settings
5. Implement token counting and advanced parameter configuration

#### B. Gemini 2.5 Integration

1. Create a new module `archon/models/gemini.py` to implement Google Gemini API integration
2. Implement a `GeminiModel` class that conforms to the same interface as existing models
3. Update model selection logic to include Gemini models
4. Add configuration options to the environment settings
5. Implement token counting and advanced parameter configuration

#### C. UI Updates

1. Modify `streamlit_pages/environment.py` to include options for Ollama and Gemini 2.5
2. Add model selection dropdown entries for these new providers
3. Add configuration fields for API keys and endpoints
4. Create UI elements for advanced parameter configuration
5. Add token budget management visualization
6. Implement performance benchmarking visualization

#### D. Enhanced Features

1. Token Budget Management
   - Implement accurate token counting for all models
   - Add safeguards to prevent context window overflows
   - Create cost estimation tools for API-based models

2. Fallback Mechanisms
   - Implement provider fallback in case of API failures
   - Create configurable fallback order
   - Add logging for fallback events

3. Security Enhancements
   - Implement secure API key storage options
   - Add documentation on security best practices
   - Create clear warnings about data privacy differences

4. Cross-Platform Compatibility
   - Test on Windows, macOS, and Linux
   - Document platform-specific considerations
   - Update Docker configuration for cross-platform deployment

#### E. Testing Strategy

1. Create unit tests for each new model integration
2. Test the full agent workflow with each model provider
3. Verify UI functionality for model selection and configuration
4. Test fallback mechanisms and error handling
5. Validate cross-platform compatibility

### Pull Request Structure

1. **Title**: "Add support for Ollama and Google Gemini 2.5 models"

2. **Description**:
   ```
   This PR adds support for two additional model providers:
   - Ollama for locally hosted open-source LLMs
   - Google Gemini 2.5 API
   
   These integrations allow users to choose from a wider variety of models beyond the current OpenAI and Anthropic options, enabling local deployment with Ollama and access to Google's latest Gemini models.
   
   Changes include:
   - New model integration classes
   - UI updates for model selection and configuration
   - Token budget management and fallback mechanisms
   - Performance benchmarking capabilities
   - Enhanced security features
   - Documentation on setup and configuration
   - Cross-platform compatibility testing
   ```

3. **Files to be modified/created**:
   - `archon/models/ollama.py` (new)
   - `archon/models/gemini.py` (new)
   - `archon/pydantic_ai_coder.py` (update)
   - `streamlit_pages/environment.py` (update)
   - `.env.example` (update)
   - Documentation files (update)
   - Test files (new)

## Architecture

### Core Components

1. **Agent Graph System**
   - `archon/archon_graph.py`: Orchestrates the multi-agent workflow
   - Implemented using LangGraph for state management
   - Defines transitions between agent states

2. **Specialized Agents**
   - `archon/pydantic_ai_coder.py`: Core agent for code generation
   - `archon/advisor_agent.py`: Recommends prebuilt tools and examples
   - `archon/refiner_agents/`: Specialized agents for different refinement tasks
     - `agent_refiner_agent.py`: Refines the overall agent implementation
     - `prompt_refiner_agent.py`: Optimizes prompt templates
     - `tools_refiner_agent.py`: Improves tool implementations

3. **Model Providers**
   - Currently supported: Anthropic (Claude) and OpenAI (GPT)
   - Planned additions: Ollama and Google Gemini 2.5
   - Future: Abstraction layer for easier integration of additional providers

4. **Tool Library**
   - `agent-resources/tools/`: Reusable tool implementations
   - `agent-resources/examples/`: Example agent implementations
   - `agent-resources/mcps/`: MCP server configurations

5. **MCP Integration**
   - `mcp/mcp_server.py`: Model Context Protocol server implementation
   - Enables connection to external services

6. **User Interface**
   - `streamlit_ui.py`: Main entry point for the Streamlit UI
   - `streamlit_pages/`: Individual UI components and pages

### Data Flow

```
User Request → Scope Definition → Component Recommendation → 
    ┌── Prompt Creation ──┐
    │   Tools Creation    │ (Parallel Execution)
    └── Agent Refinement ─┘
    → Final Integration → Deployment
```

## Coding Standards

### Python Style Guidelines

- Follow PEP 8 style guide
- Use type hints throughout the codebase
- Document functions and classes with docstrings
- Keep functions focused on a single responsibility
- Use meaningful variable and function names

### Project Structure

- Keep related files in appropriate directories
- Maintain separation of concerns between components
- Preserve iteration history in the `/iterations` directory
- New features should be developed in the core `/archon` directory

### Dependencies

- Core dependencies:
  - pydantic_ai
  - langchain
  - langchain_openai
  - langgraph
  - supabase
  - streamlit
  - logfire
  - httpx
  - python-dotenv

- Additional dependencies for new feature:
  - google-generativeai (for Gemini integration)
  - httpx or requests (for Ollama API)
  - tiktoken (for token counting)

- Use requirements.txt for dependency management
- Docker containers available for deployment

## Development Workflow

1. **Feature Planning**
   - Document new features in TASK.md
   - Consider how features integrate with existing components

2. **Implementation**
   - Develop in small, incremental changes
   - Maintain compatibility with existing functionality
   - Update documentation as features are implemented

3. **Testing**
   - Test new functionality in isolation
   - Integrate with the full system for end-to-end testing
   - Verify UI components work as expected

4. **Documentation**
   - Update inline documentation as code changes
   - Keep README.md and other documentation files current
   - Document APIs and interfaces for external use

## Extension Guidelines

### Adding New Model Providers

1. Create a new module in `archon/models/` directory
2. Implement a model class that conforms to the existing API pattern
3. Update model selection logic in relevant files
4. Add configuration options to environment settings
5. Update documentation with setup instructions
6. Implement token counting for the model
7. Create benchmarking data for performance comparison

### Adding New Tools

1. Create a new Python file in `agent-resources/tools/`
2. Follow the existing tool patterns for consistency
3. Document the tool's purpose, inputs, and outputs
4. Add examples of using the tool

### Creating New MCP Integrations

1. Add a new JSON configuration in `agent-resources/mcps/`
2. Follow the standard MCP server configuration format
3. Document the required environment variables
4. Test integration with sample agents

### Implementing New Agents

1. Add new agent implementations to appropriate directories
2. Use the Pydantic AI framework for structure
3. Consider how the agent integrates with the existing workflow
4. Document the agent's purpose and capabilities

## Environment Configuration

- Development environments should use a `.env` file
- Copy from `.env.example` and customize as needed
- Required environment variables:
  - `SUPABASE_URL`: Supabase instance URL
  - `SUPABASE_KEY`: Supabase API key
  - `ANTHROPIC_API_KEY`: Anthropic API key for Claude models
  - `OPENAI_API_KEY`: OpenAI API key for GPT models
  - `GOOGLE_API_KEY`: Google API key for Gemini models (new)
  - `GEMINI_MODEL`: Gemini model to use (new, default: gemini-2.5-pro)
  - `OLLAMA_BASE_URL`: URL for Ollama API (new, default: http://localhost:11434)
  - `OLLAMA_MODEL`: Ollama model to use (new, default: llama3)
  - `MODEL_TEMPERATURE`: Temperature setting (new, default: 0.7)
  - `MODEL_TOP_P`: Top P setting (new, default: 0.95)
  - `MODEL_MAX_TOKENS`: Maximum token output (new, default: 4096)
  - `MODEL_FALLBACK_ORDER`: Order of fallback models (new)
  - Additional keys for specific MCP integrations

## Deployment

- Docker containers available for easy deployment
- Use `run_docker.py` for local Docker deployment
- Individual components can be deployed separately if needed
- New options for Ollama integration in Docker deployment

## Future Directions

1. **Model Provider Framework**: Create a more abstracted interface for integrating LLM providers
2. **Enhanced Tool Library**: Continue expanding the prebuilt tools collection
3. **Advanced Agent Specialization**: Develop more specialized refiner agents
4. **Improved MCP Integration**: Support for more external services
5. **UI Enhancements**: Better visualization and interaction capabilities
6. **Performance Optimization**: Reduce latency and improve throughput
7. **Advanced Benchmarking**: More sophisticated model comparison tools
8. **Security Enhancements**: Better API key management and data privacy controls
