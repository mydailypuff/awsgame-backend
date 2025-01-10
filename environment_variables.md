# Environment Variables (.env) Guide

It appears you are looking for a `.env` file, but there isn't one in the workspace. Here's what you need to know:

## About .env Files
A `.env` file is commonly used to store environment variables and configuration settings that should not be committed to version control, such as:
- API keys
- Secret tokens
- Environment-specific configuration
- Other sensitive information

## Creating a .env File
1. Create a new file named `.env` in the root directory of your project
2. Add your environment variables in KEY=VALUE format, for example:
```
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
BEDROCK_MODEL_ID=anthropic.claude-v2
AWS_REGION=us-east-1
```

## Important Notes
- Never commit the `.env` file to version control
- Add `.env` to your `.gitignore` file
- Consider creating a `.env.example` file with dummy values as a template
- For AWS Lambda deployments, use Lambda environment variables instead of a .env file

## Using Environment Variables
In this project, you can access environment variables through:
1. AWS Lambda environment variables (recommended for production)
2. Local development using python-dotenv package

### Local Development
Install python-dotenv:
```bash
pip install python-dotenv
```

Load environment variables in your code:
```python
from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env file
aws_region = os.getenv('AWS_REGION')
```

### AWS Lambda Configuration
For Lambda deployments, configure environment variables in the Lambda console:
1. Go to Lambda function configuration
2. Click on "Configuration" tab
3. Select "Environment variables"
4. Add your key-value pairs

This is more secure than using a .env file in production.