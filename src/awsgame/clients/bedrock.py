"""Bedrock agent client implementation."""
import json
import os
from typing import Dict, Optional, Any

import boto3
from dotenv import load_dotenv
from botocore.exceptions import BotoCoreError, ClientError

from awsgame.exceptions.custom_exceptions import AgentValidationError, AgentCommunicationError

# Load environment variables
load_dotenv()
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

    def validate_response(self, completion: str) -> None:
        """Validate the response from the agent and clean it for JSON parsing.

        Args:
            completion: The completion string from the agent

        Raises:
            AgentValidationError: If response validation fails or JSON parsing fails
        """
        if not completion or not isinstance(completion, str):
            raise AgentValidationError("Invalid response: Completion must be a non-empty string")
            
        try:
            # Clean up the completion string by removing extra whitespace and normalizing line endings
            cleaned_completion = " ".join(completion.strip().split())
            # Parse as JSON to validate format and return cleaned version
            json.loads(cleaned_completion)
            return cleaned_completion
        except json.JSONDecodeError as e:
            raise AgentValidationError(f"Invalid JSON response: {str(e)}")

    def parse_event(self, event: dict) -> str:
        """Parse the event data and extract the game state.
        
        Args:
            event: The event dictionary containing the game state
            
        Returns:
            str: JSON string containing the structured game state
        """
        chunk_data = event.get('chunk', {}).get('bytes', b'{}')
        if isinstance(chunk_data, bytes):
            body = json.loads(chunk_data.decode('utf-8'))
        else:
            body = json.loads(chunk_data)
            
        # Extract game state components
        scene = body.get('SCENE')
        scenario = body.get('SCENARIO', {})
        scores = body.get('SCORES', {})
        game_score = body.get('GAME_SCORE')
        
        # Combine game state into structured input
        return json.dumps({
            'scene': scene,
            'scenario': scenario,
            'scores': scores,
            'game_score': game_score
        })

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
                agentId=os.getenv('BEDROCK_AGENT_ID'),
                agentAliasId=os.getenv('BEDROCK_AGENT_ALIAS_ID'),
                sessionId=session_id or 'default-session',
                inputText=user_input
            )
            
            # Extract completion from Bedrock Agent Runtime EventStream response
            completion = ""
            # Handle the streaming response
            for event in response.get('completion', []):
                if "chunk" in event:
                    chunk = event["chunk"]
                    completion += chunk["bytes"].decode()
            
            # Extract token usage information
            token_usage = response.get("usage", {})
            cleaned_completion = self.validate_response(completion)
            
            return {
                'completion': cleaned_completion,
                'session_id': response.get('sessionId')
            }
            
        except AgentValidationError:
            raise
        except Exception as e:
            raise AgentCommunicationError(f"Failed to communicate with agent: {str(e)}")