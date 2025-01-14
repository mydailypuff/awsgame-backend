# Lambda Function Setup Guide

## Configuration

1. Deploy the Lambda Function:
```bash
aws lambda create-function \
  --function-name game-backend-api \
  --runtime python3.9 \
  --handler awsgame.handlers.lambda_handler.lambda_handler \
  --role arn:aws:iam::YOUR_ACCOUNT_ID:role/game-backend-lambda-role
```

2. Update Lambda Configuration:
```bash
aws lambda update-function-configuration \
  --function-name game-backend-api \
  --timeout 30 \
  --memory-size 256 \
  --environment Variables={BEDROCK_AGENT_ID=your-agent-id,BEDROCK_AGENT_ALIAS_ID=your-alias-id}
```

3. Add Required IAM Permissions:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeAgent",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "*"
        }
    ]
}
```

## Environment Variables

- `BEDROCK_AGENT_ID`: Your Bedrock Agent ID
- `BEDROCK_AGENT_ALIAS_ID`: Your Bedrock Agent Alias ID
- `AWS_REGION`: AWS region (default: us-east-1)

## Monitoring and Logging

1. View CloudWatch Logs:
```bash
aws logs get-log-events \
  --log-group-name /aws/lambda/game-backend-api \
  --log-stream-name latest
```

2. Monitor Lambda Metrics:
```bash
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Duration \
  --dimensions Name=FunctionName,Value=game-backend-api \
  --start-time $(date -v-1H) \
  --end-time $(date) \
  --period 300 \
  --statistics Average
```

## Testing the Lambda Function

1. Direct Invocation:
```bash
aws lambda invoke \
  --function-name game-backend-api \
  --payload '{"body": "{\"user_input\": \"test message\"}"}' \
  response.json
```

2. View Response:
```bash
cat response.json
```

## Troubleshooting

1. Check Lambda Logs:
```bash
aws logs tail /aws/lambda/game-backend-api --follow
```

2. Test Lambda Configuration:
```bash
aws lambda get-function-configuration \
  --function-name game-backend-api
```