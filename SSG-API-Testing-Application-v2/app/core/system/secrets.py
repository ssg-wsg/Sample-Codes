# This code will retrieve secrets from AWS Systems Manager Parameter Store.
# The implementation is derived from the sample provided in the 'lambda' directory

import os
import streamlit as st
from tempfile import NamedTemporaryFile
import time  # noqa: E402
from app.core.system.logger import Logger

import boto3
from botocore.exceptions import ClientError

LOGGER = Logger(__name__)


# the environment names where the secrets are stored
ENV_NAME_ENCRYPT = "default_encryption_key"
ENV_NAME_CERT = "default_cert_path"
ENV_NAME_KEY = "default_key_path"

# flag to check if refetching is in progress, blank value in variable means 'false'
ENV_FLAG_REFETCH = "currently_fetching"
ENV_FLAG_LAST_FETCHED = "last_fetched"


def Refetch_secrets(refetch: bool) -> bool:
    ''' callback function for the refetch button '''
    if st.session_state["last_fetched"] < last_fetched():
        LOGGER.info("Will reuse previously fetched default secrets")
        st.session_state["secret_fetched"] = True
        st.session_state["last_fetched"] = time.time()
        return True

    if Set_Default_Secrets(refetch):
        LOGGER.info("Refetched default secrets succeeded")
        st.session_state["secret_fetched"] = True
        return True
    else:
        LOGGER.info("Refetched default secrets failed")
        st.session_state["secret_fetched"] = False
        return False


def Set_Default_Secrets(refetch: bool) -> bool:
    '''
    function to retrieve secrets and store in environment variables,
    all variables required needs to be set as environment variables in advance.

    If you do not choose to refetch, function will only set secrets if they are not set.
    If refetch is successful, clears previous secrets.
    :param refetch: should the function refetch secrets
    :return: whether defaults are avaliable to use
    '''
    if currently_fetching():
        LOGGER.warning("Abort fetching of secrets. It is already in progress")
        return False

    if not refetch and are_secrets_set():
        LOGGER.warning("Abort refetching of secrets as they are already set. "
                       "Please use the refetch option if refetching is desired.")
        return True

    swap_fetching_flag()
    LOGGER.info("Attempting to fetch secrets")
    try:
        # the path where the items are stored
        secret_path = os.environ.get('SECRET_PATH', '')
        # path to the encryption key in parameter store
        encryption_key_path = os.environ.get('SECRET_ENCRYPTION_KEY_PATH', '')
        # path to the certificate in parameter store
        cert_path = os.environ.get('SECRET_CERT_PATH', '')
        # path to the key in parameter store
        key_path = os.environ.get('SECRET_KEY_PATH', '')

        if secret_path == '':
            LOGGER.error("Environment variable for SECRET_PATH not set")
            return False
        if encryption_key_path == '':
            LOGGER.error(
                "Environment variable for SECRET_ENCRYPTION_KEY_PATH not set")
            return False
        if cert_path == '':
            LOGGER.error("Environment variable for SECRET_CERT_PATH not set")
            return False
        if key_path == '':
            LOGGER.error("Environment variable for SECRET_KEY_PATH not set")
            return False

        # the role with the permissions to obtain and decrypt secrets
        role_arn = os.environ.get('ROLE_ARN', '')
        if role_arn == '':
            LOGGER.error("Environment variable for ROLE_ARN not set")
            return False
        region_name = os.environ.get('REGION_NAME', '')
        if region_name == '':
            LOGGER.error("Environment variable for REGION_NAME not set")
            return False

        # proceed to fetch secrets
        try:
            secrets = get_secret(secret_path, role_arn, region_name)
        except Exception as e:
            LOGGER.error(f"Error occurred while fetching secrets: {str(e)}")
            return False

        if secrets is None:
            LOGGER.error(
                "No secrets found, there may not be items stored under the given secret path in parameter store")
            return False

        # get the items from the secrets response
        encryption_key = extract_secret(secrets, encryption_key_path)
        cert_value = extract_secret(secrets, cert_path)
        key_value = extract_secret(secrets, key_path)
        if encryption_key is None or cert_value is None or key_value is None:
            LOGGER.error(
                "A secret cannot be found. Please check that all secrets are stored in the given path in parameter store")
            return False

        # delete old files that you no longer need, continue even if cannot delete
        delete_file(os.environ.get(ENV_NAME_CERT, ''))
        delete_file(os.environ.get(ENV_NAME_KEY, ''))

        # seperate default cert and key from user provided by storing in current directory
        try:
            cert_pem = create_temp_file(cert_value, os.getcwd())
            key_pem = create_temp_file(key_value, os.getcwd())
            os.environ[ENV_NAME_ENCRYPT] = encryption_key
            os.environ[ENV_NAME_CERT] = cert_pem
            os.environ[ENV_NAME_KEY] = key_pem
        except Exception as e:
            LOGGER.error(
                f"Failed to set up environment variables or create temporary files: {str(e)}")
            return False

        os.environ[ENV_FLAG_LAST_FETCHED] = str(time.time())
        return True

    finally:
        swap_fetching_flag()


def are_secrets_set() -> bool:
    return os.environ.get(ENV_NAME_ENCRYPT, '') != '' and \
        os.environ.get(ENV_NAME_CERT, '') != '' and \
        os.environ.get(ENV_NAME_KEY, '') != ''


def currently_fetching() -> bool:
    return bool(os.environ.get(ENV_FLAG_REFETCH, ''))


def last_fetched() -> float:
    return float(os.environ.get(ENV_FLAG_LAST_FETCHED, '0'))


def swap_fetching_flag():
    if currently_fetching():
        os.environ[ENV_FLAG_REFETCH] = ''
    else:
        os.environ[ENV_FLAG_REFETCH] = 'fetching in progress'


def get_secret(secret_path, role_arn, region_name):
    '''
    assumes the role in the region given and returns a list of parameters found by under the secret_path
    search for your secret using the value stored in the "Name" and "Value" key
    may return None if no parameters are found
    see full response syntax at
    https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_GetParameters.html#API_GetParameters_ResponseSyntax
    '''
    # Create a Secrets Manager client
    retrieve_secrets_session = assume_role(role_arn)
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


def assume_role(role_arn):
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


def extract_secret(parameters, secret_name):
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


def create_temp_file(inputStuff, saveDir=None):
    ''' save input into temporary file and return file name '''
    temp_file = NamedTemporaryFile(
        delete=False, delete_on_close=False, suffix=".pem", dir=saveDir)
    with open(temp_file.name, 'w') as f:
        f.write(inputStuff)
    return temp_file.name


def delete_file(filePath):
    if filePath == '':
        return

    try:
        os.remove(filePath)
    except Exception as e:
        # possible errors: oserror, filenotfounderror
        # on windows, will raise exception if file is in use
        LOGGER.error(f"Error occurred while delete file {filePath}: {str(e)}")
