from pydantic_ai.models.base import BaseModel
import google.generativeai as genai
from typing import Optional, List, Dict, Any, AsyncGenerator, Union, Callable
import asyncio
import json
import tiktoken
import logging

logger = logging.getLogger(__name__)

class GeminiModel(BaseModel):
    """
    Model implementation for Google's Gemini API.
    
    This class implements the Pydantic AI model interface for Gemini models,
    allowing them to be used with Archon agents.
    """
    
    def __init__(self, model_name: str, api_key: str, **kwargs):
        """
        Initialize the Gemini model.
        
        Args:
            model_name: The name of the Gemini model to use (e.g., "gemini-2.5-pro")
            api_key: The Google API key
            **kwargs: Additional parameters
        """
        super().__init__(model_name)
        self.model_name = model_name
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
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
        
        # Prepare generation config
        generation_config = genai.types.GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_tokens if max_tokens else None,
            stop_sequences=stop_sequences if stop_sequences else None,
            top_p=kwargs.get("top_p", 0.95),
            top_k=kwargs.get("top_k", 40),
        )
        
        # Create the content parts list
        parts = []
        
        # Add system prompt if provided
        if system_prompt:
            parts.append({"role": "system", "parts": [system_prompt]})
            
        # Add user prompt
        parts.append({"role": "user", "parts": [prompt]})
        
        try:
            # Generate response
            response = await self.model.generate_content_async(
                parts,
                generation_config=generation_config,
                safety_settings=kwargs.get("safety_settings", None)
            )
            
            # Estimate token usage (approximate)
            prompt_tokens = len(self.tokenizer.encode(prompt))
            if system_prompt:
                prompt_tokens += len(self.tokenizer.encode(system_prompt))
                
            response_text = response.text
            completion_tokens = len(self.tokenizer.encode(response_text))
            
            # Return formatted response
            return {
                "text": response_text,
                "model": self.model_name,
                "finish_reason": "stop",  # Gemini doesn't provide this explicitly
                "usage": {
                    "prompt_tokens": prompt_tokens,
                    "completion_tokens": completion_tokens,
                    "total_tokens": prompt_tokens + completion_tokens
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating content with Gemini: {str(e)}")
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
        # Prepare generation config
        generation_config = genai.types.GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_tokens if max_tokens else None,
            stop_sequences=stop_sequences if stop_sequences else None,
            top_p=kwargs.get("top_p", 0.95),
            top_k=kwargs.get("top_k", 40),
        )
        
        # Create the content parts list
        parts = []
        
        # Add system prompt if provided
        if system_prompt:
            parts.append({"role": "system", "parts": [system_prompt]})
            
        # Add user prompt
        parts.append({"role": "user", "parts": [prompt]})
        
        try:
            # Generate streaming response
            stream_response = await self.model.generate_content_async(
                parts,
                generation_config=generation_config,
                stream=True,
                safety_settings=kwargs.get("safety_settings", None)
            )
            
            accumulated_text = ""
            
            # Calculate prompt tokens (approximate)
            prompt_tokens = len(self.tokenizer.encode(prompt))
            if system_prompt:
                prompt_tokens += len(self.tokenizer.encode(system_prompt))
                
            async for chunk in stream_response:
                try:
                    if hasattr(chunk, 'text') and chunk.text:
                        accumulated_text += chunk.text
                        
                        # Estimate tokens in this chunk
                        chunk_tokens = len(self.tokenizer.encode(chunk.text))
                        
                        yield {
                            "text": chunk.text,
                            "model": self.model_name,
                            "finish_reason": None,
                            "usage": {
                                "prompt_tokens": prompt_tokens,
                                "completion_tokens": len(self.tokenizer.encode(accumulated_text)),
                                "total_tokens": prompt_tokens + len(self.tokenizer.encode(accumulated_text))
                            }
                        }
                except Exception as e:
                    logger.error(f"Error processing Gemini stream chunk: {str(e)}")
                    yield {
                        "text": "",
                        "model": self.model_name,
                        "finish_reason": "error",
                        "usage": {}
                    }
                    
            # Final chunk with complete information
            yield {
                "text": "",  # Empty text for final chunk
                "model": self.model_name,
                "finish_reason": "stop",
                "usage": {
                    "prompt_tokens": prompt_tokens,
                    "completion_tokens": len(self.tokenizer.encode(accumulated_text)),
                    "total_tokens": prompt_tokens + len(self.tokenizer.encode(accumulated_text))
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating streaming content with Gemini: {str(e)}")
            yield {
                "text": f"Error generating content: {str(e)}",
                "model": self.model_name,
                "finish_reason": "error",
                "usage": {}
            }
