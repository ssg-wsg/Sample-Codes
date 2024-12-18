# This code is meant to run in AWS Lambda and will retrieve secrets from AWS Systems Manager Parameter Store.
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
    secrets = get_secret()
    
    cert = extract_secret(secrets,"/SampleApp/testing/cert")
    key = extract_secret(secrets,"/SampleApp/testing/key")    

    cert_pem = create_temp_file(cert)
    key_pem = create_temp_file(key)
    response = view_course_run(cert_pem, key_pem)
    return(response.content)


def get_secret():
    ''' 
    returns a list of parameters found by query 
    search for your secret using the value stored in the "Name" and "Value" key 
    see full response syntax at https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_GetParameters.html#API_GetParameters_ResponseSyntax 
    '''
    secret_name = "/SampleApp/testing/"
    region_name = "ap-southeast-1"

    # Create a Secrets Manager client
    retrieve_secrets_session = assume_role()
    ssm = retrieve_secrets_session.client(
        service_name='ssm',
        region_name=region_name
    )
    
    try:
        response = ssm.get_parameters_by_path(
            Path=secret_name,
            WithDecryption=True,
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_parameters_by_path.html
        raise e

    return response['Parameters']


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


def extract_secret(parameters,secret_name):
    '''
    iterate through the list of parameters 
    returns the secret value if exists and none if not found
    '''
    if parameters is None:
        return None
    
    for parameter in parameters:
        if parameter["Name"] == secret_name:
            return parameter["Value"]
    
    return None


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
