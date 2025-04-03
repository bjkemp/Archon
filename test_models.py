#!/usr/bin/env python3
"""
Test script for validating the new Ollama and Gemini model implementations.
"""
from dotenv import load_dotenv
import asyncio
import os
import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add the project directory to the path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_dir)

# Import our model implementations
from archon.models import GeminiModel, OllamaModel

async def test_gemini():
    """Test the Gemini model implementation."""
    logger.info("Testing Gemini model...")
    
    # Load API key from environment
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("LLM_API_KEY")
    if not api_key:
        logger.error("No API key found for Gemini. Set GOOGLE_API_KEY or LLM_API_KEY in your .env file.")
        return False
    
    try:
        # Initialize the model
        model_name = "gemini-2.5-pro"
        model = GeminiModel(model_name, api_key=api_key)
        logger.info(f"Initialized Gemini model: {model_name}")
        
        # Test regular completion
        prompt = "What is the capital of France? Keep it short."
        system_prompt = "You are a helpful assistant that provides concise answers."
        
        logger.info("Testing regular completion...")
        result = await model.generate(prompt, system_prompt=system_prompt)
        logger.info(f"Response: {result['text']}")
        logger.info(f"Usage: {result['usage']}")
        
        # Test streaming completion
        logger.info("Testing streaming completion...")
        stream_response = model.generate(prompt, system_prompt=system_prompt, stream=True)
        
        full_response = ""
        async for chunk in stream_response:
            if chunk.get("text"):
                full_response += chunk["text"]
                logger.info(f"Received chunk: {chunk['text']}")
        
        logger.info(f"Full streaming response: {full_response}")
        logger.info("Gemini model test completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Error testing Gemini model: {str(e)}")
        return False

async def test_ollama():
    """Test the Ollama model implementation."""
    logger.info("Testing Ollama model...")
    
    # Load configuration from environment
    base_url = os.getenv("BASE_URL") or "http://localhost:11434"
    
    try:
        # Initialize the model
        model_name = "llama3"  # Use default model
        model = OllamaModel(model_name, base_url=base_url)
        logger.info(f"Initialized Ollama model: {model_name}")
        
        # Test regular completion
        prompt = "What is the capital of France? Keep it short."
        system_prompt = "You are a helpful assistant that provides concise answers."
        
        logger.info("Testing regular completion...")
        result = await model.generate(prompt, system_prompt=system_prompt)
        logger.info(f"Response: {result['text']}")
        logger.info(f"Usage: {result['usage']}")
        
        # Test streaming completion
        logger.info("Testing streaming completion...")
        stream_response = model.generate(prompt, system_prompt=system_prompt, stream=True)
        
        full_response = ""
        async for chunk in stream_response:
            if chunk.get("text"):
                full_response += chunk["text"]
                logger.info(f"Received chunk: {chunk['text']}")
        
        logger.info(f"Full streaming response: {full_response}")
        logger.info("Ollama model test completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Error testing Ollama model: {str(e)}")
        return False

async def main():
    """Run all model tests."""
    logger.info("Starting model tests...")
    
    # Check which models to test based on environment variables
    provider = os.getenv("LLM_PROVIDER", "").lower()
    
    if provider == "gemini" or not provider:
        await test_gemini()
    
    if provider == "ollama" or not provider:
        await test_ollama()
    
    logger.info("All tests completed.")

if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())
