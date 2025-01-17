"""API Gateway utility functions."""
import json
from typing import Any, Dict, Optional

def create_response(status_code: int, body: Any, cors: bool = True) -> Dict[str, Any]:
    """Create an API Gateway response dictionary.
    
    Args:
        status_code: HTTP status code
        body: Response body
        cors: Whether to include CORS headers
        
    Returns:
        API Gateway response dictionary
    """
    # Ensure body is properly formatted for JSON
    if isinstance(body, str):
        try:
            # Try to parse as JSON first
            parsed_body = json.loads(body)
            body_to_dump = parsed_body
        except json.JSONDecodeError:
            # If not valid JSON, use the string as is
            body_to_dump = body
    else:
        body_to_dump = body

    response = {
        'statusCode': status_code,
        'body': json.dumps(body_to_dump, ensure_ascii=False)
    }
    
    if cors:
        response['headers'] = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST',
            'Access-Control-Allow-Headers': 'Content-Type'
        }
    
    return response

def parse_request_body(event: Dict[str, Any]) -> Dict[str, Any]:
    """Parse and validate the API Gateway request body.
    
    Args:
        event: API Gateway event dictionary
        
    Returns:
        Parsed request body
        
    Raises:
        ValueError: If body is invalid JSON or missing required fields
    """
    try:
        body = json.loads(event.get('body', '{}'))
        if not isinstance(body, dict):
            raise ValueError("Request body must be a JSON object")
        return body
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON in request body")