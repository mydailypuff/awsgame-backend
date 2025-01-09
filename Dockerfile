# Use AWS Lambda Python runtime as base image
FROM public.ecr.aws/lambda/python:3.9

# Set working directory
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy function code
COPY src/awsgame ./awsgame

# Set the handler
CMD ["awsgame.handlers.lambda_handler.lambda_handler"]