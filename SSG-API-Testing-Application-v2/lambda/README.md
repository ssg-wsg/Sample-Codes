# Introduction
This directory is still **WIP**

It will contain POC of obtaining secrets from AWS Secrets Manager.

This POC is meant to showcase how you can put your authentication secrets in AWS Secrets Manager and retrieve them to use when calling our APIs

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

