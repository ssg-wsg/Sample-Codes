# Deployment

This directory contains files used for deploying the Sample Application to AWS.

The code is heavily inspired and reused from [this guide](https://nexgeneerz.io/aws-computing-with-ecs-ec2-terraform/).

> [!CAUTION]
> If you are a developer, make sure to change the name of the S3 bucket used in the Terraform code to another
> unique name! If not, you will get an error as the bucket already exists.

## `create-backend`

This directory contains the Terraform code for deploying the backend of the Sample Application to AWS.

## `create-ecr`

This directory contains the Terraform code for creating the Elastic Container Registry (ECR) for the Sample Application.

## `main-infrastructure`

This directory contains the Terraform code for creating the main infrastructure of the Sample Application.

## `modules`

This directory contains the Terraform modules used in the Terraform code for deploying the Sample Application to AWS.

### `modules/constants`

This directory contains the Terraform code for defining the constants used in the Terraform code for deploying the
Sample Application to AWS.
