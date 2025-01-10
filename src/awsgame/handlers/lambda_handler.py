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
    """Handle Lambda function invocation.
    
    Args:
        event: Lambda event data
        context: Lambda context
        
    Returns:
        API Gateway response dictionary
    """
    logger.info("Lambda handler started")
    """AWS Lambda handler function.

    Args:
        event: Lambda event data
        context: Lambda context object

    Returns:
        Response dictionary with status code and body
    """
    try:
        client = BedrockAgentClient()
        user_input = client.parse_event(event)
        logger.info(f"Processing user input: {user_input}")
        session_id = None  # Session tracking not required for this flow
        logger.debug("No session tracking required - using default session")
        
        response = client.communicate(user_input, session_id)
        
        logger.info("Successfully processed request")
        logger.debug(f"Response payload: {response}")
        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }
        
    except AgentValidationError as e:
        logger.error(f"Validation error occurred: {str(e)}")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }
    except AgentCommunicationError as e:
        logger.error(f"Communication error occurred: {str(e)}", exc_info=True)
        return {
            'statusCode': 502,
            'body': json.dumps({'error': str(e)})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }