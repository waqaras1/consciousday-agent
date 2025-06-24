"""
ConsciousDay Agent - OpenAI client implementation for daily reflection and planning
"""

import os
import streamlit as st
from typing import Dict, Any, Optional
from openai import OpenAI
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class ConsciousAgent:
    """
    AI agent for processing daily reflections and generating insights
    """
    
    def __init__(self):
        """Initialize the ConsciousAgent with OpenAI client setup"""
        self.client = None
        self.api_provider = None
        self.model_name = None
        self.base_url = None
        self.http_referer = None
        
        # Initialize the agent
        self._setup_agent()
        
        if not self.client:
            raise ValueError("Failed to initialize AI agent. Please check your API configuration.")
    
    def _setup_agent(self):
        """Setup the AI agent with proper configuration"""
        is_deployed = "STREAMLIT_SERVER_PORT" in os.environ

        if is_deployed:
            openrouter_api_key = st.secrets.get("OPENROUTER_API_KEY")
            openai_api_key = st.secrets.get("OPENAI_API_KEY")
            self.http_referer = st.secrets.get("APP_URL", "https://consciousday-agent.streamlit.app")
            self.model_name = st.secrets.get("OPENROUTER_MODEL_NAME")
        else:
            openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
            openai_api_key = os.getenv('OPENAI_API_KEY')
            self.http_referer = os.getenv('APP_URL', "http://localhost:8501")
            self.model_name = os.getenv('OPENROUTER_MODEL_NAME')

        # Set default model if not specified
        if not self.model_name:
            self.model_name = "openai/gpt-3.5-turbo"

        # Set base URL for OpenRouter
        self.base_url = os.getenv('OPENROUTER_BASE_URL', "https://openrouter.ai/api/v1")

        # Try OpenRouter first, then fallback to OpenAI
        if openrouter_api_key:
            try:
                # Try with the specified model first
                self._setup_openrouter(openrouter_api_key)
                return
            except Exception as e:
                logger.warning(f"Failed to setup OpenRouter with model {self.model_name}: {e}")
                # Try with a fallback model
                try:
                    self.model_name = "openai/gpt-3.5-turbo"
                    self._setup_openrouter(openrouter_api_key)
                    logger.info(f"Successfully initialized OpenRouter with fallback model: {self.model_name}")
                    return
                except Exception as e2:
                    logger.error(f"Failed to setup OpenRouter with fallback model: {e2}")
                    if not openai_api_key:
                        raise ValueError("OpenRouter setup failed and no OpenAI API key available")
        
        if openai_api_key:
            try:
                self._setup_openai(openai_api_key)
                return
            except Exception as e:
                logger.error(f"Failed to setup OpenAI: {e}")
                raise ValueError("Failed to setup any AI provider")
        
        raise ValueError("No API key found. Set OPENROUTER_API_KEY or OPENAI_API_KEY in environment variables or Streamlit secrets.")
    
    def _setup_openrouter(self, api_key: str):
        """Setup OpenRouter configuration"""
        try:
            # Validate API key
            if not api_key or not api_key.strip():
                raise ValueError("OpenRouter API key is empty or invalid")
            
            # Validate model name
            if not self.model_name or not self.model_name.strip():
                raise ValueError("Model name is empty or invalid")
            
            logger.info(f"Attempting to initialize OpenRouter with model: {self.model_name}")
            
            self.client = OpenAI(
                base_url=self.base_url,
                api_key=api_key,
                default_headers={
                    "HTTP-Referer": self.http_referer,
                    "X-Title": "ConsciousDay Agent"
                }
            )
            self.api_provider = "OpenRouter"
            logger.info(f"Successfully initialized OpenRouter with model: {self.model_name}")
            
        except Exception as e:
            logger.error(f"Error setting up OpenRouter: {e}")
            raise
    
    def _setup_openai(self, api_key: str):
        """Setup OpenAI configuration"""
        try:
            self.client = OpenAI(api_key=api_key)
            self.api_provider = "OpenAI"
            self.model_name = "gpt-3.5-turbo"
            logger.info("Successfully initialized OpenAI")
            
        except Exception as e:
            logger.error(f"Error setting up OpenAI: {e}")
            raise
    
    def process_inputs(self, journal: str, intention: str, dream: str, priorities: str) -> str:
        """
        Process user inputs and generate AI insights
        
        Args:
            journal (str): Morning journal entry
            intention (str): Daily intention
            dream (str): Dream description
            priorities (str): Top 3 priorities
            
        Returns:
            str: AI-generated insights and strategy
        """
        try:
            # Validate inputs
            if not journal.strip() or not intention.strip() or not priorities.strip():
                raise ValueError("Missing required input fields")
            
            # Create the prompt
            prompt = f"""
You are a daily reflection and planning assistant. Your goal is to:

Reflect on the user's journal and dream input
Interpret the user's emotional and mental state
Understand their intention and 3 priorities
Generate a practical, energy-aligned strategy for their day

INPUT:
Morning Journal: {journal.strip()}
Intention: {intention.strip()}
Dream: {dream.strip() if dream.strip() else "No dream recorded"}
Top 3 Priorities: {priorities.strip()}

OUTPUT:

**Inner Reflection Summary**
[Provide a thoughtful analysis of the user's emotional and mental state based on their journal entry]

**Dream Interpretation Summary**
[Offer insights into the dream's potential meaning and how it might relate to their current situation]

**Energy/Mindset Insight**
[Analyze their energy levels and mindset, providing guidance on how to approach the day]

**Suggested Day Strategy (time-aligned tasks)**
[Create a practical, time-based strategy that aligns with their energy and priorities]

Please provide clear, actionable insights that will help the user have a more conscious and productive day.
"""
            
            # Process with AI
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful daily reflection and planning assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            if not response.choices or not response.choices[0].message.content:
                raise ValueError("AI returned empty response")
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error processing inputs: {e}")
            return f"Error processing inputs: {str(e)}"
    
    def get_agent_status(self) -> Dict[str, Any]:
        """
        Get the current status of the agent
        
        Returns:
            Dict: Status information about the agent
        """
        try:
            return {
                "status": "active" if self.client else "inactive",
                "provider": self.api_provider or "unknown",
                "model": self.model_name or "unknown",
                "temperature": 0.7,
                "base_url": self.base_url if self.api_provider == "OpenRouter" else None
            }
        except Exception as e:
            logger.error(f"Error getting agent status: {e}")
            return {
                "status": "error",
                "provider": "unknown",
                "model": "unknown",
                "error": str(e)
            }
    
    def test_connection(self) -> bool:
        """
        Test the connection to the AI provider
        
        Returns:
            bool: True if connection is successful, False otherwise
        """
        try:
            if not self.client:
                return False
            
            # Simple test with minimal input
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            return bool(response.choices and response.choices[0].message.content.strip())
            
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False
