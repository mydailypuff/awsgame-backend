import json
import logging
from agent_invocation import BedrockAgentClient
from custom_exceptions import AgentError, AgentValidationError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def lambda_handler(event: dict, context) -> dict:
    """
    AWS Lambda handler for processing Bedrock Agent requests.
    
    Args:
        event (dict): Lambda event containing request data
        context: Lambda context object
        
    Returns:
        dict: Response containing agent completion or error information
        
    Raises:
        AgentValidationError: If request validation fails
        AgentError: For other agent-related errors
    """
    try:
        # Initialize the Bedrock Agent client
        agent_client = BedrockAgentClient()
        
        # Extract user input from event
        if 'body' not in event:
            raise AgentValidationError("Missing request body")
            
        body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        
        if 'input' not in body:
            raise AgentValidationError("Missing 'input' field in request body")
            
        user_input = body['input']
        session_id = body.get('session_id')  # Optional session ID
        
        # Process request through Bedrock Agent
        response = agent_client.communicate(user_input, session_id)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(response)
        }
        
    except AgentValidationError as ve:
        logger.error(f"Validation error: {str(ve)}")
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'error': str(ve)
            })
        }
    except AgentError as ae:
        logger.error(f"Agent error: {str(ae)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'error': str(ae)
            })
        }
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'error': 'Internal server error'
            })
        }