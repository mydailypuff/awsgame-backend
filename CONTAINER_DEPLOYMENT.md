# Deploying as a Containerized Lambda Function

## Prerequisites
- AWS CLI installed and configured
- Docker installed locally
- Necessary AWS IAM permissions to push to ECR and update Lambda functions

## Steps to Deploy

1. Create an ECR repository (if not exists):
```bash
aws ecr create-repository --repository-name awsgame-lambda
```

2. Authenticate Docker to your ECR registry:
```bash
aws ecr get-login-password --region your-region | docker login --username AWS --password-stdin your-account.dkr.ecr.your-region.amazonaws.com
```

3. Build the Docker image:
```bash
docker build -t awsgame-lambda .
```

4. Tag the image:
```bash
docker tag awsgame-lambda:latest your-account.dkr.ecr.your-region.amazonaws.com/awsgame-lambda:latest
```

5. Push the image to ECR:
```bash
docker push your-account.dkr.ecr.your-region.amazonaws.com/awsgame-lambda:latest
```

6. Update or create your Lambda function to use the container image:
```bash
aws lambda create-function \
  --function-name awsgame-function \
  --package-type Image \
  --code ImageUri=your-account.dkr.ecr.your-region.amazonaws.com/awsgame-lambda:latest \
  --role arn:aws:iam::your-account:role/lambda-role

# Or update existing function
aws lambda update-function-code \
  --function-name awsgame-function \
  --image-uri your-account.dkr.ecr.your-region.amazonaws.com/awsgame-lambda:latest
```

## Important Notes
- Replace `your-region`, `your-account`, and other placeholder values with your actual AWS details
- Ensure your Lambda execution role has necessary permissions
- The container image must implement the Lambda Runtime API
- The provided Dockerfile uses the AWS provided base image which includes the Runtime API implementation

## Memory and Timeout Settings
You may need to adjust the memory and timeout settings based on your workload:
```bash
aws lambda update-function-configuration \
  --function-name awsgame-function \
  --timeout 30 \
  --memory-size 256
```