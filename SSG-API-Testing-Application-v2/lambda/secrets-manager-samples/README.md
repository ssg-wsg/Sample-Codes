This directory contains files specific to using AWS Secrets Manager instead of parameter store.

`deploy-secrets.yml` is the workflow file for github actions to deploy the secret to AWS Secret Manager

The lambda function is given the role `SampleAppLambda` with the policies below:
- AWSLambdaBasicExecutionRole (AWS managed)
- StsAssumeRole (Customer inline)

```
{
"Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "sts:AssumeRole",
            "Resource": "arn:aws:iam::YourAccountNumber:role/SampleAppRetrieveSecret"
        }
    ]
}
```

The role that the lambda function will assume when retrieving the secret from AWS Secrets Manager `SampleAppRetrieveSecret` with the policies below:
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

> [!NOTE]
> You can choose to remove the `AWSLambdaBasicExecutionRole` policy from the `SampleAppRetrieveSecret` role if logging to CloudWatch is not required. This ensures the role adheres to the principle of least privilege by only granting the permissions necessary for its task.