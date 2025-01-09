"""Unit tests for the Bedrock client."""
import pytest
from unittest.mock import MagicMock, patch

from awsgame.clients.bedrock import BedrockAgentClient
from awsgame.exceptions.custom_exceptions import AgentValidationError, AgentCommunicationError

def test_validate_input_valid():
    """Test input validation with valid input."""
    client = BedrockAgentClient()
    client.validate_input("Hello")  # Should not raise

def test_validate_input_invalid():
    """Test input validation with invalid input."""
    client = BedrockAgentClient()
    with pytest.raises(AgentValidationError):
        client.validate_input("")
    with pytest.raises(AgentValidationError):
        client.validate_input("   ")
    with pytest.raises(AgentValidationError):
        client.validate_input(None)

def test_validate_response_valid():
    """Test response validation with valid response."""
    client = BedrockAgentClient()
    client.validate_response(
        "Test response",
        {"prompt_tokens": 10, "completion_tokens": 20}
    )  # Should not raise

def test_validate_response_invalid():
    """Test response validation with invalid response."""
    client = BedrockAgentClient()
    with pytest.raises(AgentValidationError):
        client.validate_response("", {})
    with pytest.raises(AgentValidationError):
        client.validate_response("Test", None)

@patch('boto3.client')
def test_communicate_success(mock_boto3_client):
    """Test successful communication with the agent."""
    mock_response = {
        'completion': 'Test response',
        'usage': {'prompt_tokens': 10, 'completion_tokens': 20}
    }
    mock_boto3_client.return_value.invoke_agent.return_value = mock_response
    
    client = BedrockAgentClient()
    response = client.communicate("Test input", "test-session")
    
    assert response['completion'] == 'Test response'
    assert 'token_usage' in response
    assert response['session_id'] == 'test-session'

@patch('boto3.client')
def test_communicate_failure(mock_boto3_client):
    """Test failed communication with the agent."""
    mock_boto3_client.return_value.invoke_agent.side_effect = Exception("Test error")
    
    client = BedrockAgentClient()
    with pytest.raises(AgentCommunicationError):
        client.communicate("Test input")