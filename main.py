

from agent_invocation import communicate_with_agent
import json

def lambda_handler(event, context):
    try:
        # Extract the user input from the event
        body = json.loads(event.get('body', '{}'))
        user_input = body.get('input', '')
        
        # Use the session ID from the event if provided, otherwise create new
        session_id = body.get('session_id', None)
        
        # Get response from the agent
        response = communicate_with_agent(session_id, user_input)
        
        # Return the response in Lambda proxy integration format
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'response': response
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'error': str(e)
            })
        }
    