# API Gateway + Lambda Integration Setup

## Overview
This document outlines the steps to set up an API Gateway integration with the Lambda function for processing user input.

## Lambda Function Configuration
The Lambda function is already configured to handle incoming requests. The handler expects an event object that will contain the request body from API Gateway.

## API Gateway Setup Steps

1. Create a new REST API in API Gateway
```bash
aws apigateway create-rest-api --name "Game-Backend-API" --description "API for game backend interactions"
```

2. Create a POST method resource
- Create a resource for handling user input
- Configure POST method with Lambda integration
- Set the integration type as "AWS_PROXY" (Lambda Proxy integration)
- Point to the existing Lambda function

3. Configure request body mapping
- The request body should be in JSON format
- Example request body:
```json
{
    "user_input": "your message here",
    "session_id": "optional-session-id"
}
```

4. Enable CORS if needed
- Add OPTIONS method
- Add required CORS headers

5. Deploy the API
- Create a new stage (e.g., "prod" or "dev")
- Note the API endpoint URL

## Testing the API

Use curl or Postman to test the API:

```bash
curl -X POST \
  https://your-api-id.execute-api.your-region.amazonaws.com/stage/path \
  -H "Content-Type: application/json" \
  -d '{"user_input": "test message", "session_id": "test-session"}'
```

## Security Considerations

1. Consider implementing authentication/authorization
2. Use API keys if needed
3. Set up appropriate IAM roles and policies
4. Consider implementing rate limiting