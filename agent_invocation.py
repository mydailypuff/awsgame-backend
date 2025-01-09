import boto3
import json
import uuid
import os
import logging
from typing import Optional, Dict, Any, Union
from botocore.config import Config
from custom_exceptions import AgentConfigurationError, AgentValidationError, AgentCommunicationError

# Configure logging
logger = logging.getLogger(__name__)

class BedrockAgentClient:
    """Client for interacting with Amazon Bedrock Agents."""
    
    def __init__(self):
        """
        Initialize the Bedrock Agent client with configuration from environment variables.
        
        Required environment variables:
            BEDROCK_AGENT_ID: The ID of the Bedrock Agent
            BEDROCK_AGENT_ALIAS_ID: The alias ID of the Bedrock Agent
            AWS_REGION: (Optional) The AWS region to use, defaults to us-east-1
            
        Raises:
            AgentConfigurationError: If required environment variables are missing
        """
        # Get configuration from environment variables
        self.agent_id = os.environ.get('BEDROCK_AGENT_ID')
        self.agent_alias_id = os.environ.get('BEDROCK_AGENT_ALIAS_ID')
        self.region = os.environ.get('AWS_REGION', 'us-east-1')
        self.max_retries = int(os.environ.get('AWS_MAX_RETRIES', '3'))
        
        # Configure boto3 client with retry settings
        config = Config(
            region_name=self.region,
            retries={
                'max_attempts': self.max_retries,
                'mode': 'standard'
            }
        )
        
        self.bedrock_client = boto3.client('bedrock-agent-runtime', config=config)
        
        if not self.agent_id or not self.agent_alias_id:
            raise AgentConfigurationError("BEDROCK_AGENT_ID and BEDROCK_AGENT_ALIAS_ID environment variables must be set")

    def validate_input(self, user_input: str) -> None:
        """
        Validate the user input.
        
        Args:
            user_input (str): The input text to validate
            
        Raises:
            ValueError: If input validation fails
        """
        if not user_input:
            raise AgentValidationError("User input cannot be empty")
        if not isinstance(user_input, str):
            raise AgentValidationError("User input must be a string")
        if len(user_input.strip()) == 0:
            raise AgentValidationError("User input cannot be whitespace only")

    def validate_response(self, completion: str, token_usage: Dict[str, Any]) -> None:
        """
        Validate the agent response.
        
        Args:
            completion (str): The completion text from the agent
            token_usage (Dict[str, Any]): Token usage information
            
        Raises:
            ValueError: If response validation fails
        """
        if not completion:
            raise AgentValidationError("Empty response from agent")
        if not isinstance(completion, str):
            raise AgentValidationError("Invalid response format from agent")
        if not isinstance(token_usage, dict):
            raise AgentValidationError("Invalid token usage format")
        
        # Validate token usage fields
        required_fields = {'prompt_tokens', 'completion_tokens'}
        missing_fields = required_fields - set(token_usage.keys())
        if missing_fields:
            raise AgentValidationError(f"Missing required token usage fields: {missing_fields}")

    def communicate(self, user_input: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Communicate with the Bedrock Agent.

        Args:
            user_input (str): The input text to send to the agent
            session_id (Optional[str]): Session ID for continued conversations

        Returns:
            Dict[str, Any]: Response containing completion and token usage information

        Raises:
            Exception: If there's an error during agent invocation
        """
        try:
            # Validate input
            self.validate_input(user_input)
            
            # Generate a session ID if none provided
            if session_id is None:
                session_id = str(uuid.uuid4())

            # Prepare the input parameters
            input_params = {
                "agentId": self.agent_id,
                "agentAliasId": self.agent_alias_id,
                "sessionId": session_id,
                "inputText": user_input
            }

            # Invoke the Bedrock Agent
            response = self.bedrock_client.invoke_agent(**input_params)
            
            # Process the streaming response
            completion = ""
            for event in response.get("completion", []):
                if "chunk" in event:
                    chunk = event["chunk"]
                    if "bytes" in chunk:
                        completion += chunk["bytes"].decode()

            # Extract token usage information
            token_usage = response.get("usage", {})
            
            # Validate response
            self.validate_response(completion, token_usage)

            return {
                "completion": completion,
                "token_usage": token_usage,
                "session_id": session_id
            }

        except AgentValidationError:
            # Re-raise validation errors directly
            raise
        except Exception as e:
            # Convert other errors to AgentCommunicationError
            error_message = f"Error communicating with Bedrock Agent: {str(e)}"
            logger.error(error_message)
            raise AgentCommunicationError(error_message) from e



