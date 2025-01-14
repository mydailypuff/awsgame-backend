FROM public.ecr.aws/lambda/python:3.11

# Copy requirements.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install the specified packages
RUN pip install -r requirements.txt

# Copy function code
COPY src/awsgame ${LAMBDA_TASK_ROOT}/awsgame/
COPY setup.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler
CMD [ "awsgame.handlers.lambda_handler.lambda_handler" ]