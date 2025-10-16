"""
Agno agent implementation for the OpenShift Partner Labs Agents application.
"""
import json
import logging
from typing import Dict, Any, List, Optional
from agno.agent import Agent
from agno.tools import tool

from common.core.config import config
from .prompts import get_welcome_message, get_system_prompt
from .tools import (
    get_form_data,
    update_form_data,
    validate_data,
    check_form_completeness,
    submit_form,
    get_form_summary
)

if config.MODEL_TYPE == "ollama":
    from agno.models.ollama import Ollama
else:
    from agno.models.openai import OpenAIChat

logger = logging.getLogger(__name__)

class FormFillingAgent:
    """
    Main agent class that handles the form-filling conversation.
    """
    
    def __init__(self):
        self.agent = self._create_agent()
    
    def _create_agent(self) -> Agent:
        """Create and configure the Agno agent."""
        
        tools = [
            get_form_data,
            update_form_data,
            validate_data,
            check_form_completeness,
            submit_form,
            get_form_summary,
        ]
        
        # Create model based on configuration
        if config.MODEL_TYPE == "ollama":
            model = Ollama(
                id=config.OLLAMA_MODEL,
                host=config.OLLAMA_HOST,
            )
        else:
            model = OpenAIChat(
                id=config.OPENAI_MODEL,
                api_key=config.OPENAI_API_KEY,
            )
        
        # Create the agent with system prompt
        system_prompt = get_system_prompt({})  # Start with empty form data
        
        agent = Agent(
            name="OpenShift Lab Request Agent",
            model=model,
            tools=tools,
            instructions=system_prompt,
            add_history_to_context=True,
            num_history_runs=5,
            add_datetime_to_context=True,
            markdown=True,
            read_chat_history=True,  # Read chat history to maintain context
        )
        
        return agent
    
    def start_conversation(self, user_email: str) -> str:
        """
        Start a new conversation with the agent.
        
        Args:
            user_email: User's email address
            
        Returns:
            str: Welcome message from the agent
        """
        try:
            # Generate welcome message
            welcome_message = get_welcome_message(user_email)
            return welcome_message
            
        except Exception as e:
            logger.error(f"Error starting conversation: {e}")
            return f"Error starting conversation: {str(e)}"
    
    def process_message(self, message: str) -> str:
        """
        Process a user message and return agent response.

        Args:
            message: User's message

        Returns:
            str: Agent's response
        """
        try:
            # Use the agent to process the message
            response = self.agent.run(message)

            # Check if we got a valid content response
            if response and response.content:
                return response.content

            # If no content but tools were called, manually continue the conversation
            # This is a workaround for Ollama models that don't always continue after tool calls
            if hasattr(response, 'tool_calls') and response.tool_calls:
                logger.warning("Agent called tools but didn't generate response. Prompting to continue...")
                # Force the agent to continue by asking it to respond
                continue_response = self.agent.run("Please continue and ask the next question based on the tool results.")
                return continue_response.content if continue_response else "Let's continue. What information can I help you with?"

            # Fallback
            return response.content if response else "I'm processing your request. Please continue."

        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return f"Error processing message: {str(e)}"
    
    def get_form_summary(self) -> str:
        """
        Get a summary of the current form data.
        
        Returns:
            str: Form data summary
        """
        try:
            # Use the agent's get_form_summary tool
            response = self.agent.run("Please provide a summary of the current form data.")
            return response.content
            
        except Exception as e:
            logger.error(f"Error getting form summary: {e}")
            return f"Error getting form summary: {str(e)}"
    
    def submit_form(self) -> str:
        """
        Submit the completed form.
        
        Returns:
            str: Submission result
        """
        try:
            # Use the agent's submit_form tool
            response = self.agent.run("Please submit the completed form.")
            return response.content
            
        except Exception as e:
            logger.error(f"Error submitting form: {e}")
            return f"Error submitting form: {str(e)}"

# Create global instance
form_agent = FormFillingAgent()