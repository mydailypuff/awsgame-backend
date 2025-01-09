# Lambda Function Error Handling

The Lambda function has been updated to handle errors appropriately with the following status codes:

1. **400 Bad Request** - When input validation fails (AgentValidationError)
   - Invalid input format
   - Missing required fields
   - Input values out of allowed ranges

2. **502 Bad Gateway** - When communication with the Bedrock agent fails (AgentCommunicationError)
   - Connection issues with AWS Bedrock
   - Timeout from agent
   - Invalid responses from agent

3. **500 Internal Server Error** - For all other unexpected errors
   - System-level errors
   - Unhandled exceptions
   - Configuration issues

To troubleshoot specific errors:

1. Check the CloudWatch logs for the full error message and stack trace
2. Verify your input matches the expected format
3. Ensure the AWS Bedrock agent is properly configured and accessible
4. Verify your AWS credentials and permissions

The error handling has been implemented in both:
- `lambda_handler.py` - For HTTP status code mapping
- `bedrock.py` - For specific error detection and raising