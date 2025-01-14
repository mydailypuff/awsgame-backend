"""Lambda handler implementation."""
import json
import logging
from typing import Optional

from ..clients.bedrock import BedrockAgentClient
from .api_utils import create_response, parse_request_body

# Configure logging
logger = logging.getLogger(__name__)

def create_log_stream(session_id: str) -> str:
    """Create a log stream name from session ID.
    
    Args:
        session_id: Session identifier
        
    Returns:
        Log stream name
    """
    return f"session-{session_id}"

def lambda_handler(event: dict, context) -> dict:
    '''Handle Lambda function invocation from API Gateway.
    
    Args:
        event: API Gateway event data
        context: Lambda context
        
    Returns:
        API Gateway response dictionary with status code and processed response
    '''
    logger.info("Lambda handler started")
    print("Lambda handler started")
    logger.info(f"Received event: {json.dumps(event)}")
    print(event)
    try:
        logger.info(f"Received event: {json.dumps(event)}")
        # Parse and validate request body using utility function
        body = parse_request_body(event)
        user_input = body.get("user_input")
        session_id = body.get("session_id")
        
        if not user_input:
            return create_response(400, {"error": "user_input is required"})
        
        # Initialize Bedrock client and process the input
        bedrock_client = BedrockAgentClient()
        response = bedrock_client.communicate(user_input, session_id)
        
        # Return successful response using utility function
        return create_response(200, response)
        
    except ValueError as e:
        # Handle validation errors
        logger.error(f"Validation error: {str(e)}")
        return create_response(400, {"error": str(e)})
    except Exception as e:
        # Handle unexpected errors
        logger.error(f"Error processing request: {str(e)}")
        return create_response(500, {"error": str(e)})