"""Bedrock agent client implementation."""
import boto3
from typing import Dict, Any, Optional

from ..exceptions.custom_exceptions import (
    AgentConfigurationError,
    AgentValidationError,
    AgentCommunicationError
)

class BedrockAgentClient:
    """Client for interacting with Amazon Bedrock agent."""
    
    def __init__(self):
        """Initialize the Bedrock agent client."""
        try:
            self.bedrock_agent_runtime = boto3.client('bedrock-agent-runtime')
        except Exception as e:
            raise AgentConfigurationError(f"Failed to initialize Bedrock client: {str(e)}")

    def validate_input(self, user_input: str) -> None:
        """Validate the user input before sending to the agent.

        Args:
            user_input: The input string to validate

        Raises:
            AgentValidationError: If input validation fails
        """
        if not user_input or not isinstance(user_input, str):
            raise AgentValidationError("Invalid input: Input must be a non-empty string")
        
        if len(user_input.strip()) == 0:
            raise AgentValidationError("Invalid input: Input cannot be empty or whitespace")

    def validate_response(self, completion: str, token_usage: Dict[str, Any]) -> None:
        """Validate the response from the agent.

        Args:
            completion: The completion string from the agent
            token_usage: Dictionary containing token usage information

        Raises:
            AgentValidationError: If response validation fails
        """
        if not completion or not isinstance(completion, str):
            raise AgentValidationError("Invalid response: Completion must be a non-empty string")
        
        if not token_usage or not isinstance(token_usage, dict):
            raise AgentValidationError("Invalid response: Token usage must be a non-empty dictionary")

    def communicate(self, user_input: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Send a message to the agent and get the response.

        Args:
            user_input: The input string to send to the agent
            session_id: Optional session identifier

        Returns:
            Dictionary containing the agent's response and metadata

        Raises:
            AgentValidationError: If input validation fails
            AgentCommunicationError: If communication with the agent fails
        """
        try:
            self.validate_input(user_input)
            
            response = self.bedrock_agent_runtime.invoke_agent(
                agentId='YOUR_AGENT_ID',
                agentAliasId='YOUR_ALIAS_ID',
                sessionId=session_id or 'default-session',
                inputText=user_input
            )
            
            completion = response['completion']
            token_usage = response.get('usage', {})
            
            self.validate_response(completion, token_usage)
            
            return {
                'completion': completion,
                'token_usage': token_usage,
                'session_id': session_id
            }
            
        except AgentValidationError:
            raise
        except Exception as e:
            raise AgentCommunicationError(f"Failed to communicate with agent: {str(e)}")