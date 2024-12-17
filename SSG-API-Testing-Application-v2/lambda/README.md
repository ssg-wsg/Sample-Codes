# Introduction
This directory is still **WIP**

It will contain POC of obtaining secrets from AWS Systems Manager Parameter Store.

This POC is meant to showcase how you can put your authentication secrets in AWS Systems Manager Parameter Store and retrieve them to use when calling our APIs

There are also samples in the `secrets-manager-samples` folder if you wish to use AWS Secrets Manager instead.

# Description of files

`lambda_function.py` contains the lambda function POC

- Permissions given to the lambda function:
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
                "Action": [
                    "secretsmanager:GetSecretValue"
                ],
                "Resource": "*"
            }
        ]
    }
    ```

To import dependencies into AWS Lambda, you can add them via custom layers. The steps to do so are described [here](https://stackoverflow.com/questions/65975883/aws-lambda-python-error-runtime-importmoduleerror)

The minimum dependancy required to run the lambda function provided is:
- requests 

# References:
- https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html
- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_parameters_by_path.html