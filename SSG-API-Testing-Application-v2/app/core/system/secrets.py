# This code will retrieve secrets from AWS Systems Manager Parameter Store.
# The implementation is derived from the sample provided in the 'lambda' directory

from tempfile import NamedTemporaryFile  # noqa: E402

import boto3
from botocore.exceptions import ClientError

# the path where the items are stored
secret_path = "/SampleApp/testing/"
# path to the certificate parameter
cert_path = "/SampleApp/testing/cert"
# path to the key parameter
key_path = "/SampleApp/testing/key"

# the role with the permissions to obtain and decrypt secrets
role_arn = "arn:aws:iam::767397936445:role/SampleAppRetrieveSecret"
region_name = "ap-southeast-1"

# parameters that the view courses api call requires
course_run_id = "340121"
endpoint = f"https://uat-api.ssg-wsg.sg/courses/courseRuns/id/{course_run_id}"
params = {"includeExpiredCourses": "true"}
header = {
    "accept": "application/json",
    "Content-Type": "application/json"}


def lambda_handler(event, context):
    secrets = get_secret()
    
    cert_value = extract_secret(secrets,cert_path)
    key_value = extract_secret(secrets,key_path)    

    cert_pem = create_temp_file(cert_value)
    key_pem = create_temp_file(key_value)
    return


def get_secret():
    ''' 
    returns a list of parameters found by query 
    search for your secret using the value stored in the "Name" and "Value" key 
    see full response syntax at https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_GetParameters.html#API_GetParameters_ResponseSyntax 
    '''
    # Create a Secrets Manager client
    retrieve_secrets_session = assume_role()
    ssm = retrieve_secrets_session.client(
        service_name='ssm',
        region_name=region_name
    )
    
    try:
        # query the parameters under the same path
        response = ssm.get_parameters_by_path(
            Path=secret_path,
            WithDecryption=True,
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_parameters_by_path.html
        raise e

    return response['Parameters']


def assume_role():
    ''' returns a session of the temporary role to obtain the secret '''
    sts_client = boto3.client('sts')
    response = sts_client.assume_role(
        RoleArn=role_arn,
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

