"""Bedrock agent client implementation."""
import json
import os
import boto3
from typing import Dict, Any, Optional

from ..exceptions.custom_exceptions import (
    AgentConfigurationError,
    AgentValidationError,
    AgentCommunicationError
)
from ..logger import setup_logger

logger = setup_logger(__name__)

class BedrockAgentClient:
    """Client for interacting with Amazon Bedrock agent."""
    
    def __init__(self):
        """Initialize the Bedrock agent client."""
        logger.info("Initializing Bedrock agent client")
        
        # Validate required environment variables
        self.agent_id = os.getenv('BEDROCK_AGENT_ID')
        self.agent_alias_id = os.getenv('BEDROCK_AGENT_ALIAS_ID')
        
        if not self.agent_id:
            raise AgentConfigurationError("BEDROCK_AGENT_ID environment variable is required")
        if not self.agent_alias_id:
            raise AgentConfigurationError("BEDROCK_AGENT_ALIAS_ID environment variable is required")
            
        try:
            self.bedrock_agent_runtime = boto3.client('bedrock-agent-runtime')
            logger.debug("Successfully created bedrock-agent-runtime client")
        except Exception as e:
            logger.error(f"Failed to initialize Bedrock client: {str(e)}")
            raise AgentConfigurationError(f"Failed to initialize Bedrock client: {str(e)}")

    def validate_input(self, user_input: str) -> None:
        """Validate the user input.
        
        Args:
            user_input: The input string to validate
            
        Raises:
            AgentValidationError: If input validation fails
        """
        logger.debug(f"Validating user input: {user_input}")
        if len(user_input.strip()) == 0:
            logger.error("Invalid input: empty or whitespace-only string")
            raise AgentValidationError("Invalid input: Input cannot be empty or whitespace")

    def validate_response(self, completion: str) -> str:
        """Validate the response from the agent.
        
        Args:
            completion: The completion string to validate
            
        Returns:
            Cleaned completion string
            
        Raises:
            AgentValidationError: If response validation fails
        """
        logger.debug("Validating agent response")
        if not completion or not isinstance(completion, str):
            logger.error("Invalid response: not a string or empty")
            raise AgentValidationError("Invalid response: Completion must be a non-empty string")
            
        try:
            # Clean up the completion string
            cleaned_completion = " ".join(completion.strip().split())
            logger.debug("Cleaning and validating completion string")
            # Parse as JSON to validate format
            json.loads(cleaned_completion)
            logger.debug("Successfully validated response format")
            return cleaned_completion
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON response: {str(e)}"
            logger.error(error_msg)
            raise AgentValidationError(error_msg)

    def parse_event(self, event: dict) -> str:
        """Parse the event data.
        
        Args:
            event: Event dictionary
            
        Returns:
            Parsed game state as JSON string
        """
        logger.debug("Parsing incoming event data")
        logger.debug(f"Raw event: {event}")
        try:
            chunk_data = event.get('chunk', {}).get('bytes', b'{}')
            if isinstance(chunk_data, bytes):
                logger.debug("Decoding bytes chunk data")
                body = json.loads(chunk_data.decode('utf-8'))
            else:
                logger.debug("Parsing string chunk data")
                body = json.loads(chunk_data)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse event data: {str(e)}")
            body = {}
            
        # Extract game state
        scene = body.get('SCENE')
        scenario = body.get('SCENARIO', {})
        scores = body.get('SCORES', {})
        game_score = body.get('GAME_SCORE')
        
        # Create structured game state
        game_state = {
            'scene': scene,
            'scenario': scenario,
            'scores': scores,
            'game_score': game_score
        }
        logger.debug(f"Parsed game state: {game_state}")
        return json.dumps(game_state)

    def communicate(self, user_input: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Communicate with the agent.
        
        Args:
            user_input: Input string
            session_id: Optional session ID
            
        Returns:
            Response dictionary
            
        Raises:
            AgentValidationError: For validation errors
            AgentCommunicationError: For communication errors
        """
        logger.info(f"Starting communication with Bedrock agent. Session ID: {session_id or 'default-session'}")
        try:
            self.validate_input(user_input)
            
            logger.info("Invoking Bedrock agent")
            response = self.bedrock_agent_runtime.invoke_agent(
                agentId=self.agent_id,
                agentAliasId=self.agent_alias_id,
                sessionId=session_id or 'default-session',
                inputText=user_input
            )
            
            completion = ""
            logger.debug("Processing completion chunks")
            for event in response.get('completion', []):
                if "chunk" in event:
                    chunk = event["chunk"]
                    logger.debug(f"Processing chunk: {chunk}")
                    completion += chunk["bytes"].decode()
            
            token_usage = response.get("usage", {})
            logger.debug(f"Token usage: {token_usage}")
            cleaned_completion = self.validate_response(completion)
            
            return {
                'completion': cleaned_completion,
                'token_usage': token_usage
            }
            
        except Exception as e:
            error_msg = f"Agent communication failed: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise AgentCommunicationError(error_msg)