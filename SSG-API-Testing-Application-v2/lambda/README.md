# Introduction
This directory contain some samples of obtaining secrets from AWS Systems Manager Parameter Store.

This sample is meant to showcase how you can put your authentication secrets in AWS Systems Manager Parameter Store and retrieve them to use when calling our APIs.

There are also samples in the `secrets-manager-samples` folder if you wish to use AWS Secrets Manager instead.

# Explaination

## Files

`deploy-secrets.yml` is the workflow file for github actions to **DEPLOY** the secret to AWS Parameter Store.

`remove-secrets.yml` is the workflow file for github actions to **REMOVE** the secret to AWS Parameter Store.
> [!NOTE]
> While `remove-secrets.yml` works, some investigation is still needed to determine if all the variables passed via `TF_VAR_secrets` is required.

`lambda_function.py` contains the code necessary to securely retrieve secrets and interact with the View Course Run API to obtain a response.

### Running the lambda_function.py
There are some dependencies required to run this file and they are added via layers.

You only need to install the `requests` package into the custom layer.

To import dependencies into AWS Lambda, you can add them by following the steps described [here](https://stackoverflow.com/questions/65975883/aws-lambda-python-error-runtime-importmoduleerror)

### Roles and Permissions

The lambda function is given the role `SampleAppLambda` with the policies below:
- AWSLambdaBasicExecutionRole (AWS managed)
- StsAssumeRole (Customer inline) - to assume the following role to retrieve secrets 

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

The role that the lambda function will assume when retrieving the secret from AWS Parameter Store `SampleAppRetrieveSecret` with the policies below:
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
> You can choose to remove the `AWSLambdaBasicExecutionRole` policy from the `SampleAppRetrieveSecret` role if logging to CloudWatch is not required. This ensures the role adheres to the principle of least privilege by only granting the permissions necessary for its task.

# Additional References:
- https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html
- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_parameters_by_path.html
