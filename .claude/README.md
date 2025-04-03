# Archon Development with Claude

This README provides information about working with the Archon codebase using Claude as an assistant.

## Current Feature Development: Ollama and Gemini 2.5 Support

We're currently working on adding support for Ollama and Google Gemini 2.5 models to the Archon project. This feature will be developed as a pull request to the original repository.

### Development Plan

1. **Study existing model implementations**
   - Examine `archon/pydantic_ai_coder.py` and related files
   - Understand the interface requirements for model providers

2. **Implement Ollama integration**
   - Create `archon/models/ollama.py` module
   - Implement OllamaModel class
   - Add environment configuration options

3. **Implement Gemini 2.5 integration**
   - Create `archon/models/gemini.py` module
   - Implement GeminiModel class
   - Add environment configuration options

4. **Update UI and configuration**
   - Modify model selection in the Streamlit UI
   - Update environment configuration page
   - Update documentation and examples

5. **Create pull request**
   - Test thoroughly with different models
   - Document setup and usage
   - Submit PR to original repository

## Project Files

- **CLAUDE.md**: High-level overview of the Archon codebase structure and components
- **TASK.md**: Current and upcoming tasks for the Archon project
- **PLANNING.md**: Architecture, coding standards, and development workflow

## Getting Started

1. **Environment Setup**:
   ```bash
   cd /Users/kempb/Projects/Archon
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

2. **Set Up Development Branch**:
   ```bash
   git checkout -b feature/ollama-gemini-support
   ```

3. **Running the Application**:
   ```bash
   # Using Python directly
   python streamlit_ui.py
   
   # Using Docker
   python run_docker.py
   ```

4. **Development Workflow**:
   - Check TASK.md for current tasks
   - Reference PLANNING.md for architectural guidance
   - Ensure environment variables are properly configured
   - Coordinate with Claude for code generation and problem-solving

## Working with Claude

When collaborating with Claude on the Archon project:

1. **Provide Context**: Start sessions by sourcing the `.clauderc` file
   ```bash
   source /Users/kempb/Projects/Claude/.clauderc
   ```

2. **Reference Documentation**: Use the CLAUDE.md, TASK.md, and PLANNING.md files for context

3. **Code Generation**: Have Claude generate code snippets for new features or bug fixes

4. **Problem Solving**: Work with Claude to debug issues and implement solutions

5. **Documentation**: Ask Claude to document code changes and update planning documents

## Repository Management

The Archon repository is managed at `https://github.com/bjkemp/Archon.git`.

- **Local Backup Directory**: `/Users/kempb/Projects/Claude/archon_backup/`
- **Main Development Directory**: `/Users/kempb/Projects/Archon/`
- **Feature Branch**: `feature/ollama-gemini-support`

## Environment Variables

The Archon project requires several environment variables:

- `SUPABASE_URL` and `SUPABASE_KEY`: For database access
- `ANTHROPIC_API_KEY`: For Claude models
- `OPENAI_API_KEY`: For OpenAI models
- `GOOGLE_API_KEY`: For Gemini models (new)
- `OLLAMA_BASE_URL`: For Ollama models (new, default: http://localhost:11434)
- Additional variables for specific MCP integrations

These should be configured in your `.env` file.

## Project Structure Summary

- `/archon/`: Core agent implementation
  - `/archon/models/`: Model provider implementations (our new modules)
- `/iterations/`: Historical versions of the project
- `/mcp/`: Model Context Protocol server
- `/streamlit_pages/`: UI components
- `/agent-resources/`: Prebuilt tools and examples

See CLAUDE.md for a detailed overview of the project structure.
