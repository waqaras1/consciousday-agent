"""
ConsciousDay Agent - LangChain implementation for daily reflection and planning
"""

import os
import openai
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ConsciousAgent:
    """
    AI agent for processing daily reflections and generating insights
    """
    
    def __init__(self):
        """Initialize the ConsciousAgent with LangChain setup"""
        self.openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        
        if not self.openrouter_api_key and not self.openai_api_key:
            raise ValueError("Neither OPENROUTER_API_KEY nor OPENAI_API_KEY found in environment variables")
        
        if self.openrouter_api_key:
            # The correct way to configure ChatOpenAI for a custom provider like OpenRouter
            self.llm = ChatOpenAI(
                model="openai/gpt-3.5-turbo",
                temperature=0.7,
                base_url="https://openrouter.ai/api/v1",
                api_key=self.openrouter_api_key,
                default_headers={
                    "HTTP-Referer": "http://localhost:8501",
                    "X-Title": "ConsciousDay Agent"
                }
            )
            self.api_provider = "OpenRouter"
        else:
            # Use the modern ChatOpenAI class for standard OpenAI
            self.llm = ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0.7,
                api_key=self.openai_api_key
            )
            self.api_provider = "OpenAI"
        
        self.prompt_template = ChatPromptTemplate.from_template(
            template="""
You are a daily reflection and planning assistant. Your goal is to:

Reflect on the user's journal and dream input
Interpret the user's emotional and mental state
Understand their intention and 3 priorities
Generate a practical, energy-aligned strategy for their day

INPUT:
Morning Journal: {journal}
Intention: {intention}
Dream: {dream}
Top 3 Priorities: {priorities}

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
        )
        
        output_parser = StrOutputParser()
        self.chain = self.prompt_template | self.llm | output_parser
    
    def process_inputs(self, journal: str, intention: str, dream: str, priorities: str) -> str:
        """
        Process user inputs and generate AI insights
        """
        try:
            response = self.chain.invoke({
                "journal": journal,
                "intention": intention,
                "dream": dream,
                "priorities": priorities
            })
            return response.strip()

        except Exception as e:
            print(f"An exception occurred in process_inputs: {e}")
            return f"Error processing inputs: {str(e)}"
    
    def get_agent_status(self) -> Dict[str, Any]:
        """
        Get the current status of the agent
        """
        return {
            "status": "active" if (self.openrouter_api_key or self.openai_api_key) else "inactive",
            "provider": self.api_provider,
            "model": "openai/gpt-3.5-turbo" if self.api_provider == "OpenRouter" else "gpt-3.5-turbo",
            "temperature": 0.7
        } 