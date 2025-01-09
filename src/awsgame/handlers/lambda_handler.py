"""Lambda handler implementation."""
import json
from typing import Optional, Dict, Any

from ..clients.bedrock import BedrockAgentClient

def create_log_stream(session_id: str) -> str:
    """Create a new log stream name for the session.

    Args:
        session_id: Session identifier to include in log stream name

    Returns:
        Formatted log stream name
    """
    return f"agent-session-{session_id}"

def lambda_handler(event: dict, context) -> dict:
    """AWS Lambda handler function.

    Args:
        event: Lambda event data
        context: Lambda context object

    Returns:
        Response dictionary with status code and body
    """
    try:
        body = json.loads(event.get('body', '{}'))
        user_input = body.get('input')
        session_id = body.get('session_id')
        
        client = BedrockAgentClient()
        response = client.communicate(user_input, session_id)
        
        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }