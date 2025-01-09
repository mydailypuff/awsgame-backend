class AgentError(Exception):
    """Base exception for agent-related errors."""
    pass

class AgentConfigurationError(AgentError):
    """Raised when there are configuration issues."""
    pass

class AgentValidationError(AgentError):
    """Raised when input or response validation fails."""
    pass

class AgentCommunicationError(AgentError):
    """Raised when there are errors communicating with the agent."""
    pass