class AgentError(Exception):
    """Base exception for agent-related errors.
    
    This is the parent class for all agent-specific exceptions. It inherits from the built-in Exception
    class and serves as a base for more specific agent exceptions.
    
    Attributes:
        message (str): The error message describing what went wrong.
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class AgentConfigurationError(AgentError):
    """Raised when there are configuration issues with the agent.

    This exception is raised when there are problems with the agent's configuration,
    such as missing or invalid configuration parameters, incorrect settings, or
    incompatible configurations.

    Examples:
        >>> raise AgentConfigurationError("Missing required API key in configuration")
        >>> raise AgentConfigurationError("Invalid model name specified in config")

    Args:
        message (str): Detailed description of the configuration error.
    """

class AgentValidationError(AgentError):
    """Raised when input or response validation fails.

    This exception is raised when the input parameters provided to the agent
    are invalid, or when the agent's response fails validation checks. This
    can include type mismatches, out-of-range values, or invalid formats.

    Examples:
        >>> raise AgentValidationError("Input temperature must be between 0 and 1")
        >>> raise AgentValidationError("Response format does not match expected schema")

    Args:
        message (str): Detailed description of the validation error.
    """

class AgentCommunicationError(AgentError):
    """Raised when there are errors communicating with the agent.

    This exception is raised when there are network issues, timeout errors,
    API failures, or other communication problems between the application
    and the agent service.

    Examples:
        >>> raise AgentCommunicationError("Connection timeout after 30 seconds")
        >>> raise AgentCommunicationError("API returned 503 Service Unavailable")

    Args:
        message (str): Detailed description of the communication error.
        status_code (int, optional): HTTP status code if applicable.
    """
    def __init__(self, message: str, status_code: int = None):
        super().__init__(message)
        self.status_code = status_code