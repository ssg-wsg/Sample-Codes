FROM python:3.12-slim

WORKDIR /app
EXPOSE 80

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

# Below is an example command to run to set these environment variables needed for default secrets function to be set
# For more variables, just extend the command with --build-arg <ARG name>=<your value>
# For more info, see https://docs.docker.com/build/building/variables/#arg-usage-example
# docker build --build-arg SECRET_PATH="/sample/app/test" --build-arg SECRET_ENCRYPTION_KEY_PATH="/sample/app/test/encrypt" --build-arg SECRET_CERT_PATH="/sample/app/test/cert" --build-arg SECRET_KEY_PATH="/sample/app/test/key" --build-arg ROLE_ARN="arn:aws:iam::767397936445:role/SampleAppRetrieveSecret" --build-arg REGION_NAME="ap-southeast-1" -t ssg/sample-app-test .

ARG SECRET_PATH=''
ENV SECRET_PATH=$SECRET_PATH

ARG SECRET_ENCRYPTION_KEY_PATH=''
ENV SECRET_ENCRYPTION_KEY_PATH=$SECRET_ENCRYPTION_KEY_PATH

ARG SECRET_CERT_PATH=''
ENV SECRET_CERT_PATH=$SECRET_CERT_PATH

ARG SECRET_KEY_PATH=''
ENV SECRET_KEY_PATH=$SECRET_KEY_PATH

ARG ROLE_ARN=''
ENV ROLE_ARN=$ROLE_ARN

ARG REGION_NAME=''
ENV REGION_NAME=$REGION_NAME


COPY . .

ENTRYPOINT ["streamlit", "run", "Home.py"]
