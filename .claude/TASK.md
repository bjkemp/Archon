# Archon Project Tasks

## Current Tasks

- [x] Pull down latest changes from remote repository (April 3, 2025)
- [x] Create project overview documentation in CLAUDE.md (April 3, 2025)
- [x] Create project documentation with TASK.md and PLANNING.md (April 3, 2025)
- [ ] **HIGH PRIORITY**: Implement Ollama and Google Gemini 2.5 support (April 3, 2025)
  - [ ] Study existing model implementations to understand interface requirements
  - [ ] Create model directory structure and base files
  - [ ] Implement Ollama integration module
  - [ ] Implement Gemini 2.5 integration module
  - [ ] Add token counting and budget management
  - [ ] Implement fallback mechanisms between providers
  - [ ] Create performance benchmarking tools
  - [ ] Update model selection UI
  - [ ] Enhance security for API key management
  - [ ] Update environment configuration
  - [ ] Test cross-platform compatibility
  - [ ] Add documentation for new model providers
  - [ ] Prepare pull request to original repository
- [ ] Explore the latest V6 implementation and understand tool library integration
- [ ] Review MCP server implementation and test with sample agents
- [ ] Add custom .env file configurations for development environment

## Implementation Task Breakdown

### Phase 1: Core Implementation

1. [ ] Create feature branch for development
   - [ ] `git checkout -b feature/ollama-gemini-support`

2. [ ] Study existing model implementations
   - [ ] Analyze `pydantic_ai.models.anthropic.AnthropicModel`
   - [ ] Analyze `pydantic_ai.models.openai.OpenAIModel`
   - [ ] Identify common interface requirements
   - [ ] Document key methods and patterns

3. [ ] Set up model directory structure
   - [ ] Create `archon/models` directory
   - [ ] Create `archon/models/__init__.py`

4. [ ] Implement Ollama integration
   - [ ] Create `archon/models/ollama.py`
   - [ ] Implement `OllamaModel` class
   - [ ] Add streaming and non-streaming request methods
   - [ ] Implement error handling and retries
   - [ ] Add advanced parameter configuration

5. [ ] Implement Gemini integration
   - [ ] Create `archon/models/gemini.py`
   - [ ] Implement `GeminiModel` class
   - [ ] Add streaming and non-streaming request methods
   - [ ] Implement error handling and retries
   - [ ] Add advanced parameter configuration

6. [ ] Update core files
   - [ ] Modify `archon/pydantic_ai_coder.py` to use new models
   - [ ] Update model selection logic
   - [ ] Add environment variable handling

### Phase 2: Enhanced Features

7. [ ] Implement token budget management
   - [ ] Add token counting for Ollama models
   - [ ] Add token counting for Gemini models
   - [ ] Create context window overflow prevention
   - [ ] Implement cost estimation for API models

8. [ ] Create fallback mechanisms
   - [ ] Implement provider fallback on API failures
   - [ ] Add configurable fallback order
   - [ ] Create logging for fallback events

9. [ ] Develop performance benchmarking
   - [ ] Create benchmarking module
   - [ ] Implement metrics for response time, quality, and efficiency
   - [ ] Create visualization for benchmark results

10. [ ] Enhance security
    - [ ] Implement secure API key storage
    - [ ] Add data privacy controls
    - [ ] Create security documentation

### Phase 3: UI and Configuration

11. [ ] Update UI components
    - [ ] Modify `streamlit_pages/environment.py`
    - [ ] Add model provider selection options
    - [ ] Create configuration fields for new providers
    - [ ] Add advanced parameter controls
    - [ ] Implement token budget visualization

12. [ ] Update environment configuration
    - [ ] Add new variables to `.env.example`
    - [ ] Document configuration options
    - [ ] Create example configurations

13. [ ] Create example templates
    - [ ] Add templates for common Ollama models
    - [ ] Add templates for Gemini variants
    - [ ] Create use-case specific configurations

### Phase 4: Testing and Documentation

14. [ ] Implement testing
    - [ ] Create unit tests for Ollama implementation
    - [ ] Create unit tests for Gemini implementation
    - [ ] Test fallback mechanisms
    - [ ] Validate cross-platform compatibility

15. [ ] Update documentation
    - [ ] Add setup guides for new providers
    - [ ] Create usage examples
    - [ ] Document security considerations
    - [ ] Update README.md with new features

16. [ ] Prepare pull request
    - [ ] Ensure all tests pass
    - [ ] Update CHANGELOG.md
    - [ ] Create detailed PR description
    - [ ] Submit PR to original repository

## Upcoming Tasks

### Core Framework Improvements

- [ ] Add support for additional LLM providers beyond Anthropic, OpenAI, Ollama, and Gemini
- [ ] Create unified model provider abstraction layer
- [ ] Optimize performance of the agent graph system
- [ ] Implement better error handling and retry mechanisms for LLM calls
- [ ] Add unit tests for core components

### Tool Library Extensions

- [ ] Add new tools to agent-resources/tools directory
- [ ] Document existing tools with better examples
- [ ] Create additional example agents for common use cases
- [ ] Develop tool validation system to ensure tool compatibility

### UI Enhancements

- [ ] Improve chat interface with better message threading
- [ ] Add visualization for agent graph execution path
- [ ] Create more intuitive environment configuration page
- [ ] Add user authentication and profile management

### MCP Integration

- [ ] Add support for additional MCP servers
- [ ] Improve documentation for MCP server setup
- [ ] Create validation system for MCP server configurations
- [ ] Add ability to test MCP servers from the UI

### Documentation

- [ ] Improve inline documentation throughout the codebase
- [ ] Create comprehensive user guide for setting up and using Archon
- [ ] Document the system architecture in detail
- [ ] Provide examples of extending the system with custom components
- [ ] Create contributor guidelines for model provider implementations

## Discovered During Work

- [ ] Review custom modifications to archon/archon_graph.py and merge with latest changes
- [ ] Investigate purpose of custom untracked main.py and pyproject.toml files
- [ ] Determine if .python-version should be committed or kept in .gitignore

## Completed Tasks

- [x] Pull down latest changes from remote repository (April 3, 2025)
- [x] Create project overview documentation in CLAUDE.md (April 3, 2025)
- [x] Create project documentation with TASK.md and PLANNING.md (April 3, 2025)
- [x] Update planning documents with additional considerations (April 3, 2025)

## Notes

* The V6 implementation adds significant new functionality with the tool library and MCP integration
* Local modifications to archon_graph.py and requirements.txt should be reviewed to ensure compatibility
* Consider creating a development branch for local modifications instead of working directly on main
* The Ollama and Gemini integration will be developed as a feature branch for pull request to the original repository
* Security considerations are important, especially when handling API keys
* Cross-platform compatibility testing is essential, particularly for Ollama integration
