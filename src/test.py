from awsgame.clients.bedrock import BedrockAgentClient
from awsgame.exceptions.custom_exceptions import AgentError

try:
    client = BedrockAgentClient()
    response = client.communicate("SCENE_DETAILS: I am a space traveller, currently I am in mars, USER_NAME:Anuradha, USER_RACE: Female, USER_CLASS: Dumb Astronaut", "session-123")
    print(response['completion'])
except AgentError as e:
    print(f"Error: {e}")