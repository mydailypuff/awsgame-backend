import boto3
import json
import uuid

# Initialize the Bedrock Agent Runtime client (not bedrock-runtime)
bedrock_client = boto3.client('bedrock-agent-runtime', region_name='us-east-1')

# Generate a session ID for conversation continuity
session_id = str(uuid.uuid4())
agent_id = "FNMFUFHPJY"  # Replace with your Bedrock Agent ID
agent_alias_id = "TSTALIASID"  # You need to specify your agent alias ID

def communicate_with_agent(session_id, user_input):
    # Prepare the input parameters
    input_params = {
        "agentId": agent_id,
        "agentAliasId": agent_alias_id,  # Required parameter
        "sessionId": session_id,
        "inputText": user_input
    }

    # Invoke the Bedrock Agent
    response = bedrock_client.invoke_agent(**input_params)
    #print(response)
    
    completion = ""
     # Handle the streaming response
    for event in response.get("completion"):
        if "chunk" in event:
            chunk = event["chunk"]
            completion += chunk["bytes"].decode()
    token_usage = response.get("usage", {})
    print("Token Usage:", token_usage)

    
    return completion

# Example interaction
user_input = "Lets Start"
response = communicate_with_agent(session_id, user_input)
print("Agent Response:", response)



