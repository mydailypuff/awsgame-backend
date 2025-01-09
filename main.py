import json
import logging
import datetime
import boto3
from agent_invocation import BedrockAgentClient
from custom_exceptions import AgentError, AgentValidationError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize CloudWatch Logs client
cloudwatch_logs = boto3.client('logs')
LOG_GROUP_NAME = '/aws/lambda/bedrock-agent-handler'  # This should be configured as needed

def create_log_stream(session_id: str) -> str:
    """
    Create a new log stream with a structured name format.
    
    Args:
        session_id (str): The session ID for the request
        
    Returns:
        str: The name of the created log stream
    """
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    stream_name = f"{timestamp}-{session_id}"
    
    try:
        cloudwatch_logs.create_log_stream(
            logGroupName=LOG_GROUP_NAME,
            logStreamName=stream_name
        )
    except cloudwatch_logs.exceptions.ResourceAlreadyExistsException:
        # Stream already exists, which is fine
        pass
    
    return stream_name

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
            
        request_time = datetime.datetime.now().isoformat()
            
        body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        
        if 'input' not in body:
            raise AgentValidationError("Missing 'input' field in request body")
            
        user_input = body['input']
        session_id = body.get('session_id') or str(context.aws_request_id)  # Use request ID if no session ID
        
        # Create log stream for this request
        log_stream_name = create_log_stream(session_id)
        
        # Log request details
        cloudwatch_logs.put_log_events(
            logGroupName=LOG_GROUP_NAME,
            logStreamName=log_stream_name,
            logEvents=[
                {
                    'timestamp': int(datetime.datetime.now().timestamp() * 1000),
                    'message': json.dumps({
                        'event': 'request',
                        'timestamp': request_time,
                        'session_id': session_id,
                        'input': user_input
                    })
                }
            ]
        )
        
        # Process request through Bedrock Agent
        response = agent_client.communicate(user_input, session_id)
        
        # Log response
        cloudwatch_logs.put_log_events(
            logGroupName=LOG_GROUP_NAME,
            logStreamName=log_stream_name,
            logEvents=[
                {
                    'timestamp': int(datetime.datetime.now().timestamp() * 1000),
                    'message': json.dumps({
                        'event': 'response',
                        'timestamp': datetime.datetime.now().isoformat(),
                        'session_id': session_id,
                        'completion': response['completion'],
                        'token_usage': response['token_usage']
                    })
                }
            ]
        )
        
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