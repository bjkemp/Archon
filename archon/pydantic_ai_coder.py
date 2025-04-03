from __future__ import annotations as _annotations

from dataclasses import dataclass
from dotenv import load_dotenv
import logfire
import asyncio
import httpx
import os
import sys
import json
from typing import List
from pydantic import BaseModel
from pydantic_ai import Agent, ModelRetry, RunContext
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.models.openai import OpenAIModel
from openai import AsyncOpenAI
from supabase import Client

# Add the parent directory to sys.path to allow importing from the parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.utils import get_env_var
from archon.agent_prompts import primary_coder_prompt
from archon.agent_tools import (
    retrieve_relevant_documentation_tool,
    list_documentation_pages_tool,
    get_page_content_tool
)
# Import our new model classes
from archon.models import GeminiModel, OllamaModel

load_dotenv()

provider = get_env_var('LLM_PROVIDER') or 'OpenAI'
llm = get_env_var('PRIMARY_MODEL') or 'gpt-4o-mini'
base_url = get_env_var('BASE_URL') or 'https://api.openai.com/v1'
api_key = get_env_var('LLM_API_KEY') or 'no-llm-api-key-provided'
google_api_key = get_env_var('GOOGLE_API_KEY') or None

# Select model based on provider
if provider == "Anthropic":
    model = AnthropicModel(llm, api_key=api_key)
elif provider == "Gemini":
    model = GeminiModel(llm, api_key=google_api_key or api_key)
elif provider == "Ollama":
    model = OllamaModel(llm, base_url=base_url, api_key=None if api_key == "NOT_REQUIRED" else api_key)
else:  # Default to OpenAI
    model = OpenAIModel(llm, base_url=base_url, api_key=api_key)

logfire.configure(send_to_logfire='if-token-present')

@dataclass
class PydanticAIDeps:
    supabase: Client
    embedding_client: AsyncOpenAI
    reasoner_output: str
    advisor_output: str

pydantic_ai_coder = Agent(
    model,
    system_prompt=primary_coder_prompt,
    deps_type=PydanticAIDeps,
    retries=2
)

async def list_docs_pages(self: RunContext):
    return await list_documentation_pages_tool(self)

async def get_docs_page(self: RunContext, page_name: str):
    return await get_page_content_tool(self, page_name)

async def rag_query(self: RunContext, query: str) -> str:
    return await retrieve_relevant_documentation_tool(self, query)

pydantic_ai_coder.register_tool("list_documentation_pages", list_docs_pages, timeout=60, retry=ModelRetry(max_retries=3))
pydantic_ai_coder.register_tool("get_page_content", get_docs_page, timeout=60, retry=ModelRetry(max_retries=3))
pydantic_ai_coder.register_tool("retrieve_relevant_documentation", rag_query, timeout=60, retry=ModelRetry(max_retries=3))

async def run_pydantic_ai_coder(deps: PydanticAIDeps, query: str):
    return await pydantic_ai_coder.run(deps, query)
