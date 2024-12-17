# This code is meant to run in AWS Lambda and will retrieve secrets from AWS Parameter Store.
# Use this code snippet in your app.
# If you need more information about configurations
# or implementing the sample code, visit the AWS docs:
# https://aws.amazon.com/developer/language/python/

import certifi
import requests
import json
from tempfile import NamedTemporaryFile  # noqa: E402

import boto3
from botocore.exceptions import ClientError

course_run_id = "35423"
endpoint = f"https://uat-api.ssg-wsg.sg/courses/courseRuns/id/{course_run_id}"
params = {"includeExpiredCourses": "true"}
header = {
    "accept": "application/json",
    "Content-Type": "application/json"}


def lambda_handler(event, context):
    secrets = json.loads(get_secret())
    cert_pem = create_temp_file(secrets["cert"])
    key_pem = create_temp_file(secrets["key"])
    response = view_course_run(cert_pem, key_pem)
    print(response)


def get_secret():

    secret_name = "SampleApp/testing"
    region_name = "ap-southeast-1"

    # Create a Secrets Manager client
    retrieve_secrets_session = assume_role()
    session = boto3.session.Session()
    client = retrieve_secrets_session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret = get_secret_value_response['SecretString']

    # Your code goes here.
    return secret


def assume_role():
    sts_client = boto3.client('sts')
    response = sts_client.assume_role(
        RoleArn="arn:aws:iam::767397936445:role/SampleAppRetrieveSecret",
        RoleSessionName="retrieve-secret-session"
    )

    new_session = boto3.Session(aws_access_key_id=response['Credentials']['AccessKeyId'],
                                aws_secret_access_key=response['Credentials']['SecretAccessKey'],
                                aws_session_token=response['Credentials']['SessionToken'])

    return new_session


def create_temp_file(inputStuff):
    ''' save input into temporary file and return file name '''
    temp_file = NamedTemporaryFile(
        delete=False, delete_on_close=False, suffix=".pem")
    with open(temp_file.name, 'w') as f:
        f.write(inputStuff)
    return temp_file.name


def view_course_run(cert_pem, key_pem):
    return requests.get(endpoint,
                        params=params,
                        headers=header,
                        verify=certifi.where(),
                        cert=(cert_pem, key_pem))
