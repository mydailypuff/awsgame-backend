"""Custom exception classes for the AWS Game Backend."""

class AgentError(Exception):
    """Base class for agent-related exceptions."""

    def __init__(self, message: str):
        """Initialize the exception.

        Args:
            message: Error message
        """
        self.message = message
        super().__init__(self.message)

class AgentConfigurationError(AgentError):
    """Exception raised for agent configuration errors."""

    def __init__(self, message: str):
        """Initialize the exception.

        Args:
            message: Error message describing the configuration issue
        """
        super().__init__(f"Configuration error: {message}")

class AgentValidationError(AgentError):
    """Exception raised for input/output validation errors."""

    def __init__(self, message: str):
        """Initialize the exception.

        Args:
            message: Error message describing the validation issue
        """
        super().__init__(f"Validation error: {message}")

class AgentCommunicationError(AgentError):
    """Exception raised for communication errors with the agent."""

    def __init__(self, message: str, status_code: int = None):
        """Initialize the exception.

        Args:
            message: Error message describing the communication issue
            status_code: Optional HTTP status code
        """
        error_msg = f"Communication error: {message}"
        if status_code:
            error_msg += f" (Status code: {status_code})"
        super().__init__(error_msg)
        self.status_code = status_code