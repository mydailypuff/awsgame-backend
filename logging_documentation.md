# Logging Implementation Documentation

This document describes the logging implementation across the AWS Game Backend.

## Overview

The application uses Python's built-in logging module with a centralized configuration through `src/awsgame/logger.py`. Logs are configurable via the `LOG_LEVEL` environment variable.

## Log Levels

- DEBUG: Detailed information for debugging
- INFO: General operational events
- ERROR: Error conditions that might still allow the application to continue running
- CRITICAL: Critical errors that prevent proper functioning

## Key Components with Logging

### BedrockAgentClient
- Initialization and configuration
- Input validation
- Response processing
- API communication
- Error handling

### Lambda Handlers
- Request processing
- Response generation
- Error handling and status codes

### Exception Classes
- Configuration errors
- Validation errors
- Communication errors

## Best Practices Implemented

1. Consistent logging format across all modules
2. Environment-based log level configuration
3. Contextual information in log messages
4. Error traceability
5. Performance impact consideration

## Example Log Messages

```
2023-XX-XX HH:MM:SS,SSS - awsgame.clients.bedrock - INFO - Initializing Bedrock agent client
2023-XX-XX HH:MM:SS,SSS - awsgame.handlers.lambda_handler - INFO - Lambda handler started
2023-XX-XX HH:MM:SS,SSS - awsgame.exceptions.custom_exceptions - ERROR - Validation error: Invalid input
```

## Troubleshooting

### Common Error Patterns

1. **Client Initialization Failures**
```
awsgame.clients.bedrock - ERROR - Failed to initialize Bedrock client: Could not connect to the endpoint URL
```
Check AWS credentials and network connectivity.

2. **Input Validation Errors**
```
awsgame.clients.bedrock - ERROR - Invalid input: empty or whitespace-only string
```
Ensure input meets validation requirements.

3. **JSON Parsing Issues**
```
awsgame.clients.bedrock - ERROR - Failed to parse event data: Expecting value: line 1 column 1
```
Verify JSON format in request payloads.

### Log Level Selection

- Use DEBUG for development and troubleshooting
- Use INFO for general operation monitoring
- Use ERROR for production error tracking

### Performance Considerations

- DEBUG level logging includes detailed payload information and should be used carefully in production
- Consider using sampling for high-volume debug logging
- Use structured logging fields for easier parsing