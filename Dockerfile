# Use Python 3.9 slim base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy package files
COPY pyproject.toml setup.py requirements.txt ./
COPY src/ ./src/

# Install dependencies and package
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir .

# Set Python path
ENV PYTHONPATH=/app/src

# Run the Lambda handler
CMD ["python", "-m", "awslambdaric", "awsgame.handlers.lambda_handler.lambda_handler"]