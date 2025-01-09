# Docker Configuration Troubleshooting Guide

## Dockerfile Overview
The current Dockerfile is configured correctly with:
- AWS Lambda Python 3.9 runtime base image
- Proper working directory setup using `${LAMBDA_TASK_ROOT}`
- Requirements installation
- Source code copying
- Lambda handler configuration

## Common Issues and Solutions

1. **Missing requirements.txt**
   - Ensure requirements.txt exists in the root directory
   - File should contain all required dependencies including:
     - boto3
     - Any other AWS SDK dependencies
     - Additional project dependencies

2. **Permission Issues**
   - Make sure the files have correct permissions
   - Docker build user should have access to all required files
   - Lambda execution role should have necessary AWS permissions

3. **Build Context**
   - Run docker build from the project root directory
   - All paths in COPY commands are relative to build context

4. **Lambda Handler Path**
   - Verify the handler path matches your code structure
   - Current: "awsgame.handlers.lambda_handler.lambda_handler"
   - Format: "{module}.{file}.{function}"

5. **Build Command**
```bash
docker build -t awsgame-lambda .
```

6. **Testing Locally**
```bash
docker run -p 9000:8080 awsgame-lambda
```

7. **Environment Variables**
   - If needed, add them using:
   ```dockerfile
   ENV VARIABLE_NAME=value
   ```

## Deployment Checklist
1. [ ] All required files present in build context
2. [ ] requirements.txt is up to date
3. [ ] Lambda handler path is correct
4. [ ] Proper AWS permissions configured
5. [ ] Dependencies properly installed
6. [ ] Local testing successful