# Dockerfile for Extractor Lambda
# ─────────────────────────────────────────────────────────────
# We use the official AWS Lambda Python 3.12 base image.
# This base image includes the AWS Lambda Runtime Interface Client (RIC),
# allowing the container to communicate seamlessly with the Lambda service.
# ─────────────────────────────────────────────────────────────

FROM public.ecr.aws/lambda/python:3.12

# Copy requirements file and install dependencies to container root
COPY requirements.txt ${LAMBDA_TASK_ROOT}/
RUN pip install --no-cache-dir -r requirements.txt

# Copy function code into Lambda task root directory
COPY handler.py ${LAMBDA_TASK_ROOT}/

# Set the CMD to your handler (filename.function_name)
CMD [ "handler.handler" ]
