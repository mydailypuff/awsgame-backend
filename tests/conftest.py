"""Pytest configuration and fixtures."""
import pytest
from unittest.mock import MagicMock

@pytest.fixture
def mock_bedrock_client():
    """Create a mock Bedrock client for testing."""
    return MagicMock()