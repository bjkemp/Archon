# Ollama and Google Gemini 2.5 Support - Feature Implementation Plan

## Overview

This document outlines the detailed implementation plan for adding support for Ollama and Google Gemini 2.5 models to the Archon project. This feature will enable users to leverage locally hosted open-source LLMs via Ollama and Google's latest Gemini models as alternatives to the currently supported OpenAI and Anthropic models.

## Implementation Steps

### 1. Development Environment Setup

1. Create a feature branch:
   ```bash
   git checkout -b feature/ollama-gemini-support
   ```

2. Update dependencies in requirements.txt:
   ```
   google-generativeai>=0.3.0  # For Gemini API
   httpx>=0.25.0               # For HTTP requests to Ollama API
   tiktoken>=0.5.1             # For token counting
   ```

### 2. Study Existing Implementation

Examine the current model implementation in:
- `archon/pydantic_ai_coder.py` 
- `pydantic_ai.models.anthropic.AnthropicModel`
- `pydantic_ai.models.openai.OpenAIModel`

Key elements to understand:
- Interface requirements for model classes
- Model initialization and configuration
- Request handling and response processing
- Error handling and retry mechanisms

### 3. Create Model Directory Structure

```bash
mkdir -p archon/models
touch archon/models/__init__.py
```

### 4. Ollama Model Implementation

#### 4.1 Create Ollama Model Module

Create `archon/models/ollama.py` with:

- `OllamaModel` class that conforms to the same interface as `AnthropicModel` and `OpenAIModel`
- Configuration handling for Ollama API URL and model selection
- Methods for sending requests to Ollama API
- Response processing and error handling

#### 4.2 Key Features to Implement

1. Initialization with configurable model name and API URL
2. Streaming and non-streaming request methods
3. Proper handling of system prompts and chat messages
4. Error handling and retries
5. Token counting and usage tracking
6. Advanced parameter configuration (temperature, top_p, etc.)

### 5. Google Gemini 2.5 Implementation

#### 5.1 Create Gemini Model Module

Create `archon/models/gemini.py` with:

- `GeminiModel` class that conforms to the same interface as other model classes
- Configuration handling for Google API key and model selection
- Methods for sending requests to Google Gemini API
- Response processing and error handling

#### 5.2 Key Features to Implement

1. Initialization with configurable model name and API key
2. Streaming and non-streaming request methods
3. Proper handling of system prompts and chat messages
4. Error handling and retries
5. Token counting and usage tracking
6. Advanced parameter configuration (temperature, top_p, etc.)

### 6. Update Core Files

#### 6.1 Update `archon/pydantic_ai_coder.py`

1. Import new model classes:
   ```python
   from archon.models.ollama import OllamaModel
   from archon.models.gemini import GeminiModel
   ```

2. Add model initialization and selection logic to support new providers
3. Update relevant agent creation and handling code to work with new models

#### 6.2 Update Environment Configuration

1. Add new environment variables to `.env.example`:
   ```
   # Google Gemini API
   GOOGLE_API_KEY=your_google_api_key_here
   GEMINI_MODEL=gemini-2.5-pro
   
   # Ollama
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=llama3
   
   # Advanced Parameters (optional)
   MODEL_TEMPERATURE=0.7
   MODEL_TOP_P=0.95
   MODEL_MAX_TOKENS=4096
   MODEL_FALLBACK_ORDER=ANTHROPIC,OPENAI,GEMINI,OLLAMA
   ```

2. Update environment loading code to handle new variables

### 7. Update UI

#### 7.1 Modify `streamlit_pages/environment.py`

1. Add UI elements for configuring Ollama:
   - Base URL input
   - Model selection dropdown
   - Model parameter controls (temperature, etc.)

2. Add UI elements for configuring Gemini:
   - API key input
   - Model selection dropdown
   - Model parameter controls (temperature, etc.)

3. Update model provider selection UI to include new options
4. Add fallback configuration options
5. Add token budget management UI elements

### 8. Performance and Security Features

#### 8.1 Performance Benchmarking

1. Create a benchmarking module to compare model performance:
   - Response time
   - Quality of responses
   - Token efficiency

2. Implement a UI page for benchmark results visualization

#### 8.2 Token Budget Management

1. Implement token counting for Ollama and Gemini models
2. Add safeguards to prevent context window overflows
3. Create token usage visualization in the UI
4. Add cost estimation for API-based models

#### 8.3 Security Enhancements

1. Implement secure API key storage options
2. Add documentation on security best practices
3. Create clear warnings about data privacy differences between local and cloud models

#### 8.4 Fallback Mechanisms

1. Implement provider fallback in case of API failures
2. Create configurable fallback order
3. Add logging for fallback events

### 9. Testing

#### 9.1 Unit Tests

1. Create test files:
   - `tests/models/test_ollama.py`
   - `tests/models/test_gemini.py`

2. Implement tests for:
   - Model initialization
   - Request formatting
   - Response handling
   - Error conditions
   - Fallback mechanisms
   - Token counting accuracy

#### 9.2 Integration Tests

1. Test full agent workflow with each model provider
2. Verify UI functionality for model selection and configuration
3. Test cross-platform compatibility (Windows, macOS, Linux)

### 10. Documentation

#### 10.1 Add New Model Documentation

1. Update README.md with information about the new model providers
2. Create setup guides for Ollama and Gemini
3. Update environment configuration documentation
4. Create model-specific usage examples
5. Document security considerations and best practices

#### 10.2 Update Code Documentation

1. Add detailed docstrings to new model classes and methods
2. Include examples of using each model provider
3. Document common troubleshooting scenarios

#### 10.3 Contributor Guidelines

1. Create a template for future model provider implementations
2. Document the process for adding new model providers
3. Outline testing requirements for model contributions

### 11. Deployment Enhancements

1. Update Docker configuration to optionally include Ollama
2. Document Docker deployment options:
   - Ollama in the same container
   - Ollama via container networking
   - Cloud-only deployment options

### 12. Pull Request Preparation

1. Ensure all tests pass
2. Update CHANGELOG.md with new feature information
3. Prepare PR description with detailed information about the changes
4. Create PR to original repository

## APIs and Integration Details

### Ollama API

- Base URL: `http://localhost:11434` (default)
- API Endpoint: `/api/chat`
- Request Format:
  ```json
  {
    "model": "llama3",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Hello, who are you?"}
    ],
    "stream": true,
    "options": {
      "temperature": 0.7,
      "top_p": 0.95,
      "top_k": 40,
      "num_predict": 128
    }
  }
  ```
- Response Format:
  ```json
  {
    "model": "llama3",
    "created_at": "2023-11-06T10:09:43.01911742Z",
    "message": {
      "role": "assistant",
      "content": "I am Llama, an AI assistant..."
    },
    "done": true,
    "total_duration": 2030941125,
    "load_duration": 1125,
    "prompt_eval_count": 26,
    "prompt_eval_duration": 321663875,
    "eval_count": 68,
    "eval_duration": 1708885500
  }
  ```

### Google Gemini API

- API Library: `google-generativeai`
- Model: `gemini-2.5-pro` (default)
- Key Features:
  - System instructions support
  - Function calling
  - Streaming responses
  - Safety settings

- Basic Usage:
  ```python
  import google.generativeai as genai
  
  genai.configure(api_key="YOUR_API_KEY")
  model = genai.GenerativeModel('gemini-2.5-pro')
  response = model.generate_content("Hello, who are you?")
  ```

- Advanced Configuration:
  ```python
  generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 2048,
  }
  
  model = genai.GenerativeModel(
    'gemini-2.5-pro',
    generation_config=generation_config
  )
  ```

## Cross-Platform Compatibility

### Windows Considerations

- Ensure proper handling of path separators
- Test with Windows-hosted Ollama
- Document Windows-specific installation steps

### macOS Considerations

- Test with macOS-hosted Ollama
- Verify Apple Silicon compatibility
- Document macOS-specific installation steps

### Linux Considerations

- Test with Linux-hosted Ollama
- Verify Docker deployment on Linux
- Document Linux-specific installation steps

## Examples and Templates

### Ollama Model Templates

- Default configuration templates for common models:
  - Llama models (Llama 3, etc.)
  - Mistral models (Mistral 7B, etc.)
  - Code-specific models (CodeLlama, etc.)

### Gemini Model Templates

- Configuration templates for Gemini variants:
  - Gemini 2.5 Pro
  - Gemini 2.5 Flash
  - Domain-specific configurations

## Timeline

1. **Week 1**: Study existing implementation and create model modules
2. **Week 2**: Update core files and UI integration
3. **Week 3**: Implement performance, security, and fallback features
4. **Week 4**: Testing, documentation, and pull request preparation

## Success Criteria

1. Users can successfully use Ollama-hosted models with Archon
2. Users can successfully use Google Gemini 2.5 models with Archon
3. The UI properly supports configuration of these new model providers
4. Performance benchmarking helps users choose appropriate models
5. Fallback mechanisms ensure reliability when API calls fail
6. Token budget management prevents context window overflows
7. Documentation clearly explains how to set up and use the new models
8. All tests pass with the new model providers on all major platforms
