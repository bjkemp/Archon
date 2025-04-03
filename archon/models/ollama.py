from pydantic_ai.models.base import BaseModel
from typing import Optional, List, Dict, Any, AsyncGenerator, Union, Callable
import httpx
import asyncio
import json
import tiktoken
import logging
from urllib.parse import urljoin

logger = logging.getLogger(__name__)

class OllamaModel(BaseModel):
    """
    Model implementation for Ollama API.
    
    This class implements the Pydantic AI model interface for Ollama models,
    allowing locally hosted open-source LLMs to be used with Archon agents.
    """
    
    def __init__(self, model_name: str, base_url: str = "http://localhost:11434", api_key: Optional[str] = None, **kwargs):
        """
        Initialize the Ollama model.
        
        Args:
            model_name: The name of the Ollama model to use (e.g., "llama3")
            base_url: The base URL for the Ollama API (default: "http://localhost:11434")
            api_key: Optional API key if Ollama is configured to require it
            **kwargs: Additional parameters
        """
        super().__init__(model_name)
        self.model_name = model_name
        self.base_url = base_url
        self.api_key = api_key
        self.tokenizer = tiktoken.encoding_for_model("gpt-4")  # Use GPT-4 tokenizer as approximation
        
    async def generate(self, 
                      prompt: str, 
                      system_prompt: Optional[str] = None,
                      temperature: float = 0.7,
                      max_tokens: Optional[int] = None,
                      stop_sequences: Optional[List[str]] = None,
                      stream: bool = False,
                      **kwargs) -> Union[Dict[str, Any], AsyncGenerator[Dict[str, Any], None]]:
        """
        Generate a response from the model.
        
        Args:
            prompt: The prompt to send to the model
            system_prompt: Optional system prompt to prepend
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum number of tokens to generate
            stop_sequences: Sequences that will stop generation
            stream: Whether to stream the response
            **kwargs: Additional parameters
            
        Returns:
            Either a complete response dict or an async generator of response chunks
        """
        if stream:
            return self._generate_stream(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=temperature,
                max_tokens=max_tokens,
                stop_sequences=stop_sequences,
                **kwargs
            )
            
        # Create the messages array
        messages = []
        
        # Add system prompt if provided
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
            
        # Add user prompt
        messages.append({"role": "user", "content": prompt})
        
        # Prepare the request payload
        payload = {
            "model": self.model_name,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,
                "top_p": kwargs.get("top_p", 0.95),
                "top_k": kwargs.get("top_k", 40),
            }
        }
        
        # Add num_predict (max_tokens) if specified
        if max_tokens:
            payload["options"]["num_predict"] = max_tokens
            
        # Add stop if specified
        if stop_sequences:
            payload["options"]["stop"] = stop_sequences
            
        # Prepare headers
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
            
        try:
            # Make the request to Ollama API
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    urljoin(self.base_url, "/api/chat"),
                    json=payload,
                    headers=headers
                )
                
                # Check if the request was successful
                response.raise_for_status()
                
                # Parse the response
                result = response.json()
                
                # Extract the response text
                response_text = result.get("message", {}).get("content", "")
                
                # Estimate token usage (approximate)
                prompt_tokens = len(self.tokenizer.encode(prompt))
                if system_prompt:
                    prompt_tokens += len(self.tokenizer.encode(system_prompt))
                    
                completion_tokens = len(self.tokenizer.encode(response_text))
                
                # Return formatted response
                return {
                    "text": response_text,
                    "model": self.model_name,
                    "finish_reason": "stop",
                    "usage": {
                        "prompt_tokens": prompt_tokens,
                        "completion_tokens": completion_tokens,
                        "total_tokens": prompt_tokens + completion_tokens,
                        # Include Ollama-specific metrics if available
                        "eval_count": result.get("eval_count", 0),
                        "eval_duration": result.get("eval_duration", 0),
                        "total_duration": result.get("total_duration", 0)
                    }
                }
                
        except Exception as e:
            logger.error(f"Error generating content with Ollama: {str(e)}")
            return {
                "text": f"Error generating content: {str(e)}",
                "model": self.model_name,
                "finish_reason": "error",
                "usage": {}
            }
            
    async def _generate_stream(self,
                              prompt: str,
                              system_prompt: Optional[str] = None,
                              temperature: float = 0.7,
                              max_tokens: Optional[int] = None,
                              stop_sequences: Optional[List[str]] = None,
                              **kwargs) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Stream a response from the model.
        
        Args:
            prompt: The prompt to send to the model
            system_prompt: Optional system prompt to prepend
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum number of tokens to generate
            stop_sequences: Sequences that will stop generation
            **kwargs: Additional parameters
            
        Yields:
            Response chunks as dictionaries
        """
        # Create the messages array
        messages = []
        
        # Add system prompt if provided
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
            
        # Add user prompt
        messages.append({"role": "user", "content": prompt})
        
        # Prepare the request payload
        payload = {
            "model": self.model_name,
            "messages": messages,
            "stream": True,
            "options": {
                "temperature": temperature,
                "top_p": kwargs.get("top_p", 0.95),
                "top_k": kwargs.get("top_k", 40),
            }
        }
        
        # Add num_predict (max_tokens) if specified
        if max_tokens:
            payload["options"]["num_predict"] = max_tokens
            
        # Add stop if specified
        if stop_sequences:
            payload["options"]["stop"] = stop_sequences
            
        # Prepare headers
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
            
        try:
            # Calculate prompt tokens (approximate)
            prompt_tokens = len(self.tokenizer.encode(prompt))
            if system_prompt:
                prompt_tokens += len(self.tokenizer.encode(system_prompt))
                
            # Make the streaming request to Ollama API
            async with httpx.AsyncClient(timeout=120.0) as client:
                async with client.stream(
                    "POST",
                    urljoin(self.base_url, "/api/chat"),
                    json=payload,
                    headers=headers
                ) as response:
                    # Check if the request was successful
                    response.raise_for_status()
                    
                    accumulated_text = ""
                    
                    # Process streaming response
                    async for chunk in response.aiter_lines():
                        if not chunk:
                            continue
                            
                        try:
                            chunk_data = json.loads(chunk)
                            
                            # Extract the message content
                            chunk_text = chunk_data.get("message", {}).get("content", "")
                            
                            if chunk_text:
                                accumulated_text += chunk_text
                                
                                # Estimate tokens in this chunk
                                chunk_tokens = len(self.tokenizer.encode(chunk_text))
                                
                                yield {
                                    "text": chunk_text,
                                    "model": self.model_name,
                                    "finish_reason": None,
                                    "usage": {
                                        "prompt_tokens": prompt_tokens,
                                        "completion_tokens": len(self.tokenizer.encode(accumulated_text)),
                                        "total_tokens": prompt_tokens + len(self.tokenizer.encode(accumulated_text))
                                    }
                                }
                                
                            # Check if this is the final chunk
                            if chunk_data.get("done", False):
                                # Final chunk with complete information
                                yield {
                                    "text": "",  # Empty text for final chunk
                                    "model": self.model_name,
                                    "finish_reason": "stop",
                                    "usage": {
                                        "prompt_tokens": prompt_tokens,
                                        "completion_tokens": len(self.tokenizer.encode(accumulated_text)),
                                        "total_tokens": prompt_tokens + len(self.tokenizer.encode(accumulated_text)),
                                        # Include Ollama-specific metrics if available
                                        "eval_count": chunk_data.get("eval_count", 0),
                                        "eval_duration": chunk_data.get("eval_duration", 0),
                                        "total_duration": chunk_data.get("total_duration", 0)
                                    }
                                }
                                break
                                
                        except json.JSONDecodeError:
                            logger.error(f"Error decoding JSON from Ollama stream: {chunk}")
                            continue
                        except Exception as e:
                            logger.error(f"Error processing Ollama stream chunk: {str(e)}")
                            yield {
                                "text": "",
                                "model": self.model_name,
                                "finish_reason": "error",
                                "usage": {}
                            }
                            break
                            
        except Exception as e:
            logger.error(f"Error generating streaming content with Ollama: {str(e)}")
            yield {
                "text": f"Error generating content: {str(e)}",
                "model": self.model_name,
                "finish_reason": "error",
                "usage": {}
            }
