# Setting Environment Variables in Lambda Containers

There are several ways to set environment variables for a containerized Lambda function:

1. **Using the Dockerfile:**
   ```dockerfile
   ENV MY_VARIABLE=my_value
   ```
   This sets environment variables during container build time.

2. **Using Lambda Console or AWS CLI:**
   Configure environment variables in the Lambda function configuration:
   ```bash
   aws lambda update-function-configuration \
     --function-name YOUR_FUNCTION_NAME \
     --environment "Variables={KEY1=value1,KEY2=value2}"
   ```

3. **Using Container Runtime Settings:**
   Add environment variables to your Lambda function configuration when creating or updating the function:
   ```bash
   aws lambda create-function \
     --function-name YOUR_FUNCTION_NAME \
     --package-type Image \
     --code ImageUri=YOUR_ECR_IMAGE_URI \
     --environment "Variables={KEY1=value1,KEY2=value2}" \
     --role YOUR_LAMBDA_ROLE_ARN
   ```

4. **Using AWS Systems Manager Parameter Store:**
   For sensitive information, you can use Parameter Store and access variables at runtime:
   ```python
   import boto3
   
   def get_parameter(param_name):
       ssm = boto3.client('ssm')
       response = ssm.get_parameter(Name=param_name, WithDecryption=True)
       return response['Parameter']['Value']
   ```

Best Practices:
- Use Lambda environment variables for non-sensitive configuration
- Use AWS Secrets Manager or Parameter Store for sensitive information
- Environment variables set in the Lambda configuration override those set in the Dockerfile
- Remember that environment variables are encrypted at rest and in transit
- Maximum size for all environment variables is 4 KB

Note: Changes to environment variables require a new deployment of your Lambda function.