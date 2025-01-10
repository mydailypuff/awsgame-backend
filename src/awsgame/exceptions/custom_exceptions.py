"""Custom exception classes for the AWS Game Backend."""
from ..logger import setup_logger

logger = setup_logger(__name__)

class AgentError(Exception):
    """Base exception class for agent-related errors."""
    
    def __init__(self, message: str):
        """Initialize the exception.
        
        Args:
            message: The error message
        """
        logger.error(f"Agent error occurred: {message}")
        super().__init__(message)

class AgentConfigurationError(AgentError):
    """Exception raised for agent configuration errors."""
    
    def __init__(self, message: str):
        """Initialize the exception."""
        logger.error(f"Configuration error: {message}")
        super().__init__(message)

class AgentValidationError(AgentError):
    """Exception raised for validation errors."""
    
    def __init__(self, message: str):
        """Initialize the exception."""
        logger.error(f"Validation error: {message}")
        super().__init__(message)

class AgentCommunicationError(AgentError):
    """Exception raised for communication errors."""
    
    def __init__(self, message: str, status_code: int = None):
        """Initialize the exception."""
        logger.error(f"Communication error (status_code={status_code}): {message}")
        self.status_code = status_code
        super().__init__(message)