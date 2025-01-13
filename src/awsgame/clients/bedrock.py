"""Bedrock agent client implementation."""

import json
import logging
from typing import Any, Dict, Optional

import boto3

from ..exceptions.custom_exceptions import (
    AgentValidationError,
    AgentCommunicationError
)
from ..logger import get_logger

logger = get_logger(__name__)

class BedrockAgentClient:
    """AWS Bedrock agent client."""

    def __init__(self):
        """Initialize the client."""
        from awsgame.config import BEDROCK_AGENT_ID, BEDROCK_AGENT_ALIAS_ID
        
        if not BEDROCK_AGENT_ID:
            raise AgentConfigurationError(
                "BEDROCK_AGENT_ID environment variable is not set. "
                "Please set it with a valid agent ID from your AWS Console. "
                "See SETUP.md for instructions."
            )
            
        self.agent_id = BEDROCK_AGENT_ID
        self.agent_alias_id = BEDROCK_AGENT_ALIAS_ID
        logger.info(f"Initialized Bedrock agent client with agent_id={self.agent_id}, alias_id={self.agent_alias_id}")

    def validate_input(self, user_input: str) -> None:
        """Validate the input string."""
        if not user_input or not isinstance(user_input, str):
            raise AgentValidationError("Input must be a non-empty string")

    def validate_response(self, completion: str) -> str:
        """Validate and clean the response string."""
        if completion is None:
            raise AgentValidationError("Response cannot be None")
        if not isinstance(completion, str):
            raise AgentValidationError(f"Response must be a string, got {type(completion)}")
        cleaned = str(completion).strip()
        if not cleaned:
            raise AgentValidationError("Response cannot be empty")
        return cleaned

    def communicate(self, user_input: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Send a synchronous request to the Bedrock agent.
        
        Args:
            user_input: User input text
            session_id: Optional session identifier
            
        Returns:
            Dictionary with agent response
        """
        self.validate_input(user_input)
        
        try:
            # Create basic client for synchronous operations
            client = boto3.client('bedrock-agent-runtime', region_name='us-east-1')
            logger.info(f"Attempting to invoke Bedrock agent (id={self.agent_id}, alias={self.agent_alias_id})")
            
            # Make basic synchronous request
            response = client.invoke_agent(
                agentId=self.agent_id,
                agentAliasId=self.agent_alias_id,
                sessionId=session_id or 'default-session',
                inputText=user_input
            )
            
            # Handle event stream response
            if not response or 'completion' not in response:
                raise AgentValidationError("No completion found in Bedrock agent response")
            

            # Process the event stream
            completion_text = ""
            
            for event in response.get('completion'):
                if "chunk" in event:
                    chunk = event["chunk"]
                    completion_text += chunk['bytes'].decode('utf-8')
            
            logger.debug(f"Received completion from Bedrock: {completion_text}")
            
            cleaned_response = self.validate_response(completion_text)
            return {'response': cleaned_response}
            
        except client.exceptions.ResourceNotFoundException as e:
            logger.error(f"Bedrock agent not found: {str(e)}")
            raise AgentCommunicationError(
                f"Agent with ID '{self.agent_id}' and alias '{self.agent_alias_id}' not found. "
                "Please verify your configuration and ensure the agent exists and is active. "
                "See TROUBLESHOOTING.md for more details."
            )
        except (AgentValidationError, client.exceptions.ClientError) as e:
            logger.error(f"Error communicating with Bedrock: {str(e)}")
            raise AgentCommunicationError(str(e))
        
# if __name__ == "__main__":
#     client = BedrockAgentClient()
#     response = client.communicate("SCENE_DETAILS: I am a space traveller, currently I am in mars, USER_NAME:Anuradha, USER_RACE: Female, USER_CLASS: Dumb Astronaut")
#     print(response)