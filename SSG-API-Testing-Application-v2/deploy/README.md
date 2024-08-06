# Deployment

This directory contains files used for deploying the Sample Application to AWS.

The code is heavily inspired and reused from [this guide](https://nexgeneerz.io/aws-computing-with-ecs-ec2-terraform/).

> [!CAUTION]
> If you are a developer, make sure to change the name of the S3 bucket used in the Terraform code under `dev` 
> to another unique name!
> 
> Other developers may have already used the bucket name described within the Terraform code, and using the same
> bucket name will raise an error since S3 bucket names must be unique!

## `dev`

This folder contains the Terraform code for deploying the Sample Application to AWS in the `dev` environment.

The `dev` environment is used by developers to test the Sample Application, and experiment with infrastructural
changes that poses the risk of breaking the `prod` (production) environment.

## `prod`

This folder contains the Terraform code for deploying the Sample Application to AWS in the `prod` environment.

The `prod` environment is where the application will be deployed and accessed by our users.

Changes to infrastructure should not be directly made to the `prod` environment. Instead, changes should be made to the
`dev` environment first, and tested there. Once the changes are confirmed to be working, the changes should be applied
to the `prod` environment, pending review.

## `modules`

This directory contains the Terraform modules used in the Terraform code for deploying the Sample Application to AWS.

### `modules/constants`

This directory contains the Terraform code for defining the constants used in the Terraform code for deploying the
Sample Application to AWS.

## `ssh`

This folder contains the SSH public keys that are used to access the EC2 instances that are created by the
Terraform code.
