# Introduction
This directory contain some samples of obtaining secrets from AWS Systems Manager Parameter Store.

This is a minimal sample and is meant to showcase how you can put your authentication secrets in AWS Systems Manager Parameter Store and retrieve them to use when calling our APIs.

There are also samples in the `secrets-manager-samples` folder if you wish to use AWS Secrets Manager instead.

# Brief overview

## Workflow / deployment files
`deploy` directory contains the terraform code for the automated deployment to AWS.

Please ensure that the `working-directory:` parameter in the workflow files is pointing to the `deploy` directory as these two files work together.

`deploy-secrets.yml` is the workflow file for github actions to **DEPLOY** the secret to AWS Parameter Store.

`remove-secrets.yml` is the workflow file for github actions to **REMOVE** the secret from AWS Parameter Store.

> [!NOTE]
> While `remove-secrets.yml` works, some investigation is still needed to determine if all the variables passed via `TF_VAR_secrets` is required.

AWS credentials and environment variables (containing the secrets) are required for the workflow to function.

Please refer to the `GitHub Actions` section under the `Deployment Guide` in the Sample App v2 docs for guidance on how to place these into Github environment secrets.

You can put these files into the `.github/workflows` directory and the workflow will appear under Github Actions. 

## Lambda function example
`lambda_function.py` contains the code necessary to securely retrieve secrets and interact with the View Course Run API to obtain a response.


# Running the lambda_function.py
There are three main steps to perform to be able to run the Lambda function in `lambda_function.py`.
1. Create parameters
2. Create Roles and Permissions
3. Install dependencies

Please refer to the sections below if you need guidance with setting up the lambda function.

After performing these steps, the code in `lambda_function.py` can be directly copied into your AWS lambda function and executed.

> [!NOTE]
> You may be prompted for a 'test event' when trying to execute. You may use the default options as this event is ignored by the sample code.

## Create parameters

AWS Parameter Store will store the secrets that the lambda function will use when it is executing.

The configuration of the parameters used by the sample is **"Standard"** tier and stored as **"SecureString"** type.

Please refer to the AWS documentation [here](https://docs.aws.amazon.com/systems-manager/latest/userguide/parameter-create-console.html) for steps on how to store your secrets in parameter store.

## Create Roles and Permissions

The lambda function requires two IAM roles in order to function, one for itself and one to retrieve secrets so as to align with best practices.

Please refer to the AWS documentation [here](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-service.html) if you need guidance on how to create IAM roles.

The lambda function itself requires the IAM role `SampleAppLambda` with the policies below:
- AWSLambdaBasicExecutionRole (AWS managed)
- StsAssumeRole (Customer inline) - to assume the `SampleAppRetrieveSecret` role to retrieve secrets 

```
{
"Version": "2012-10-17","Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "sts:AssumeRole",
            "Resource": "arn:aws:iam::YourAccountNumber:role/SampleAppRetrieveSecret"
        }
    ]
}
```

Another role named `SampleAppRetrieveSecret` that the lambda function will assume when retrieving the secret from AWS Parameter Store with the policies below:
- AWSLambdaBasicExecutionRole (AWS managed) 
- KmsDecrypt 
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "kms:Decrypt",
            "Resource": "*"
        }
    ]
}
```
- SecretsPolicy  
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "ssm:GetParametersByPath",
            "Resource": "arn:aws:ssm:ap-southeast-1:767397936445:parameter/SampleApp/*"
        }
    ]
}
```

> [!NOTE]
> You can choose to remove the `AWSLambdaBasicExecutionRole` policy from the `SampleAppRetrieveSecret` role if logging to CloudWatch is not required. 

## Install dependencies
There are additional dependencies required to run the Lambda function and they need to be added via 'layers'.

To do so, please install the `requests` package into a custom layer.

To install and import the custom layer with the dependency into AWS Lambda, you can add them by following the steps described [here](https://stackoverflow.com/questions/65975883/aws-lambda-python-error-runtime-importmoduleerror)

# Additional References:
- https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html
- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_parameters_by_path.html
