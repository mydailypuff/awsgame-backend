"""Lambda handler implementation."""
import json
from typing import Optional, Dict, Any

from ..clients.bedrock import BedrockAgentClient
from ..exceptions.custom_exceptions import AgentValidationError, AgentCommunicationError

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
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }
    except AgentCommunicationError as e:
        return {
            'statusCode': 502,
            'body': json.dumps({'error': str(e)})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }