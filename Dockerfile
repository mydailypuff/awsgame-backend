FROM public.ecr.aws/lambda/python:3.12

# Install the dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy the env file inside the container, Later migrate it to jenkins config
COPY . ./

# Set the CMD to your handler
CMD ["main.lambda_handler"]