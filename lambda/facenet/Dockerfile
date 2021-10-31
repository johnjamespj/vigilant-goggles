FROM public.ecr.aws/lambda/python:3.8

# Install the function's dependencies using file requirements.txt
# from your project folder.

COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Copy function code
COPY src/* ${LAMBDA_TASK_ROOT}/

# run embedding.py locally to download models locally before creating img
COPY models/* ${LAMBDA_TASK_ROOT}/models/

COPY keras_facenet/__init__.py ${LAMBDA_TASK_ROOT}/keras_facenet

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.handler" ] 