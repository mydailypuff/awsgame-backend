# User Input Analysis

## Input Processing Flow

1. The API Gateway receives a POST request with JSON body containing:
   - `user_input`: The message from the user (required)
   - `session_id`: Optional session identifier for conversation continuity

2. The Lambda function processes the request by:
   - Validating the presence of required fields
   - Ensuring proper JSON formatting
   - Checking for input sanitization via BedrockAgentClient.validate_input()

3. The BedrockAgentClient:
   - Validates the input format and content
   - Communicates with AWS Bedrock service
   - Returns structured response

## Input Validation

The system performs multiple levels of validation:

1. API Gateway Level:
   - Ensures proper HTTP method (POST)
   - Validates Content-Type header
   - Checks basic JSON structure

2. Lambda Level:
   - Validates presence of required fields
   - Handles missing or malformed input
   - Provides appropriate error responses

3. BedrockAgent Level:
   - Validates input length and content
   - Ensures safe processing
   - Handles service-specific requirements

## Error Handling

The system provides detailed error responses for various scenarios:

- 400 Bad Request: Missing or invalid input
- 500 Internal Server Error: Processing or service errors
- Specific error messages in response body

## Testing Scenarios

Test your input processing with these cases:

1. Valid input:
```bash
curl -X POST \
  https://your-api-endpoint/stage/process \
  -H "Content-Type: application/json" \
  -d '{"user_input": "What is the current status?"}'
```

2. Missing required field:
```bash
curl -X POST \
  https://your-api-endpoint/stage/process \
  -H "Content-Type: application/json" \
  -d '{}'
```

3. With session continuity:
```bash
curl -X POST \
  https://your-api-endpoint/stage/process \
  -H "Content-Type: application/json" \
  -d '{"user_input": "Continue from previous", "session_id": "abc123"}'
```