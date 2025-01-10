"""Lambda handler implementation."""
import json
from typing import Optional, Dict, Any

from ..clients.bedrock import BedrockAgentClient
from ..exceptions.custom_exceptions import AgentValidationError, AgentCommunicationError
from ..logger import setup_logger

logger = setup_logger(__name__)

def create_log_stream(session_id: str) -> str:
    """Create a new log stream name for the session.
    
    Args:
        session_id: Session identifier
    
    Returns:
        Log stream name
    """
    return f"game-session-{session_id}"

def lambda_handler(event: dict, context) -> dict:
    """AWS Lambda handler function.

    Args:
        event: Lambda event data
        context: Lambda context object

    Returns:
        Response dictionary with status code and body
    """
    logger.info("New Lambda handler started")
    logger.debug(f"Received event: {event}")
    try:
        client = BedrockAgentClient()
        user_input = client.parse_event(event)
        print(f"Received input: {user_input}")
        session_id = None  # Session tracking not required for this flow
        
        response = client.communicate(user_input, session_id)
        
        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }
        
    except AgentValidationError as e:
        error_response = {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }
        logger.debug(f"Returning error response: {error_response}")
        return error_response
    except AgentCommunicationError as e:
        logger.error(f"Communication error in new handler: {str(e)}", exc_info=True)
        error_response = {
            'statusCode': 502,
            'body': json.dumps({'error': str(e)})
        }
        logger.debug(f"Returning error response: {error_response}")
        return error_response
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }