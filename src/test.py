import asyncio
from awsgame.clients.bedrock import BedrockAgentClient
from awsgame.exceptions.custom_exceptions import AgentError

def main():
    try:
        client = BedrockAgentClient()
        response = client.communicate("SCENE_DETAILS: I am a space traveller, currently I am in mars, USER_NAME:Anuradha, USER_RACE: Female, USER_CLASS: Dumb Astronaut", "session-123")
        print(response['response'])
    except AgentError as e:
        print(f"Error: {e}")
        print("\nPlease check SETUP.md and TROUBLESHOOTING.md for configuration instructions.")

if __name__ == "__main__":
    main()