# API Testing Guide

## Prerequisites
1. Deployed Lambda function
2. Configured API Gateway
3. API endpoint URL
4. Postman or curl installed (for testing)

## Test Cases

### 1. Basic Request
```bash
curl -X POST \
  https://your-api-endpoint/stage/process \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "Hello, how can you help me today?"
  }'
```
Expected result: 200 OK with response from Bedrock agent

### 2. Request with Session
```bash
curl -X POST \
  https://your-api-endpoint/stage/process \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "Continue our conversation",
    "session_id": "test-session-123"
  }'
```
Expected result: 200 OK with contextual response

### 3. Missing User Input
```bash
curl -X POST \
  https://your-api-endpoint/stage/process \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test-session-123"
  }'
```
Expected result: 400 Bad Request with error message

### 4. Invalid JSON
```bash
curl -X POST \
  https://your-api-endpoint/stage/process \
  -H "Content-Type: application/json" \
  -d '{invalid json}'
```
Expected result: 400 Bad Request with parsing error message

### 5. CORS Preflight
```bash
curl -X OPTIONS \
  https://your-api-endpoint/stage/process \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: POST"
```
Expected result: 200 OK with CORS headers

## Response Format
Successful response:
```json
{
  "statusCode": 200,
  "headers": {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "OPTIONS,POST",
    "Access-Control-Allow-Headers": "Content-Type"
  },
  "body": {
    "response": "Agent response here",
    "session_id": "session-id-if-provided"
  }
}
```

Error response:
```json
{
  "statusCode": 400,
  "headers": {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*"
  },
  "body": {
    "error": "Error message here"
  }
}
```