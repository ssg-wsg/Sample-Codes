# Deployment Guide

Welcome to the SSG-WSG Sample Application Deployment Guide!

## Table of Contents

1. [Usage of the Guide](#usage-of-the-guide)
2. [AWS](#aws)
    1. [Preparation](#preparation)
3. [Codecov](#codecov)
4. [GitHub](#github)
    1. [GitHub Actions](#github-actions)
        1. [Workflows](#workflows)
    2. [Preparation](#preparation-1)
5. [Docker](#docker)
    1. [Images and Dockerfiles](#images-and-dockerfiles)
    2. [Docker Commands](#docker-commands)
        1. [`docker build`](#docker-build)
        2. [`docker run`](#docker-run)
6. [Terraform](#terraform)
    1. [Install Terraform](#install-terraform)
    2. [Terraform Configuration](#terraform-configuration)
        1. [`create-backend`](#create-backend)
        2. [`main-infrastructure`](#main-infrastructure)
    3. [Terraform Modules](#terraform-modules)
    4. [Terraform Plan](#terraform-plan)
    5. [Terraform Apply](#terraform-apply)
    6. [Terraform Destroy](#terraform-destroy)
7. [Cloud Architecture](#cloud-architecture)
    1. [Services](#services)
        1. [EC2](#ec2)
        2. [ECR](#ecr)
        3. [ECS](#ecs)
        4. [Fargate](#fargate)
        5. [Elastic Load Balancer](#elastic-load-balancer)
    2. [Production Architecture](#production-architecture)

## Usage of the Guide

To aid you in understanding how to deploy the Sample Application, notes, warnings and hints are added to this user guide
to help you better understand the different aspects of the Sample Application.

Text in **green** callout boxes are some tips and tricks that you should be aware of while using the Sample Application:

> [!TIP]
> This is a tip!

Text in **blue** callout boxes are informational messages that you should take note of:

> [!NOTE]
> This is a note!

Text in **yellow** callout boxes are warnings that you should take note of to ensure that you do not encounter an error:

> [!WARNING]
> This is a warning!

Text in **red** callout boxes are potential errors which you may encounter while performing an action in the
Sample Application:

> [!CAUTION]
> This is a potential error!

The following section details some of the tools that we are using to deploy the application to AWS.

## AWS

Amazon Web Services (AWS) is a cloud computing platform that provides a wide range of cloud services, including
computing power, storage, databases, machine learning, and more.

For the Sample Application, we will be deploying it on AWS to take advantage of the scalability, reliability, and
security that AWS provides.

### Preparation

Before you can deploy the Sample Application to AWS, follow the steps below to prepare your AWS account:

1. Create an AWS account if you do not already have one. Follow the instructions provided in
   this [forum post](https://repost.aws/knowledge-center/create-and-activate-aws-account)
   for more information on how you can create an AWS account.
2. Create an IAM user with the necessary permissions to deploy the Sample Application. Follow the instructions provided
   in this [guide](https://medium.com/@sam.xzo.developing/create-aws-iam-user-02ee9c65c877) to create an IAM user. Make sure to attach
   the [AdministratorAccess](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AdministratorAccess.html)
   policy to the IAM user to ensure the user has the necessary permissions to deploy the Sample Application.
    1. This is important as you are highly advised against using the root account to change your AWS resources.

> [!WARNING]
> Even though you are also recommended to keep permissions as minimal as possible, for the purposes of this guide, you
> are advised to attach the `AdministratorAccess` policy to the IAM user to ensure that you have the necessary
> permissions to deploy the Sample Application.

3. Create an Access Key and Secret Key for the IAM user. Follow the instructions in
   the [AWS documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html)
   to create an Access Key and Secret Key for the IAM user.

> [!CAUTION]
> Make sure NOT to check the key files or any other files containing your keys into version control or share them
> with anyone! This is to prevent unauthorised access to your AWS resources.

After obtaining your secret key and access key, you are ready to move on to the next step of the preparation
process on GitHub. Refer to the [GitHub section](#GitHub) for more information on what you need to do for the next step.

## Codecov

Codecov is a code coverage tool that helps you measure the effectiveness of your tests by showing you which parts of
your code is being tested and which parts are not.

For the Sample Application, we will be using Codecov to measure the code coverage of the tests that are run on the
application.

To use Codecov, you will need to create an account on Codecov and link your GitHub repository to Codecov. Follow
[this guide](https://docs.codecov.com/docs/quick-start) to get started with Codecov.

Make sure to save the Repository Upload Token, as it will be used in the next section to configure the GitHub Actions
workflows.

## GitHub

GitHub is a code hosting platform for version control and collaboration. It lets you and others work together on
projects from anywhere.

For the Sample Application, we will be using GitHub to host the codebase and to automate the deployment process using
GitHub Actions.

In addition to GitHub, we will also be using GitHub Actions to automate the testing and deployment processes to AWS.

GitHub Actions is a Continuous Integration/Continuous Deployment tool that allows you to automate your software
development workflows. You can use GitHub Actions to build, test, and deploy your code right from GitHub.

### GitHub Actions

GitHub Actions allow you to specify workflows that are triggered by events in your GitHub repository by using YML files
that declare the resources, actions and triggers that are used to trigger a workflow.

GitHub Actions workflows are stored in the `.github/workflows` directory at the root of the repository.

> [!NOTE]
> Workflows can be automatically triggered by events such as a push (commit) to the repository, a pull request, or
> a new release. Workflows can also be **manually triggered** by using the `workflow_dispatch` event.
>
> For `workflow_dispatch` events, you can trigger a workflow by going to the Actions tab in your repository, selecting
> the workflow that you want to run, and click the `Run workflow` button.
>
> Note that `workflow_dispatch` workflows can be triggered manually only if the workflow YML file exists in the
> `main`/`master` branch of the repository!

#### Workflows

Workflows are declared within a YML file. Sections within the YML file determine the actions, as well as the sequence,
to take when the workflow is triggered.

Most importantly, there are a few declarations that you should be aware of when creating a workflow:

* `on`: This declaration specifies the event that triggers the workflow. For example, a push to the repository, a pull
  request, or a new release.
* `env`: This declaration specifies the environment variables that are used in the workflow. Environment variables can
  either be
  secrets (which should never be exposed to the workflow in plaintext) or global variables that we want to keep
  consistent across
  the workflow.
* `jobs`: This declaration specifies the jobs that are run in the workflow. Jobs are a high-level collection of steps to
  take to complete a task.
    * Jobs are run in parallel by default, but you can specify dependencies between jobs to run them in sequence.
      under the [GitHub Actions Marketplace](https://github.com/marketplace?type=actions).
* `steps`: This declaration specifies the steps that are run in the job. Steps are a collection of tasks that are run in
  sequence to complete the job.
* `strategy`, `matrix`: These declarations specify the matrix of configurations that are used to run the workflow. This
  is
  useful when you want to run the same workflow with different configurations in parallel.
* `runs-on`: This declaration specifies the runner that the job runs on. The runner is the environment that the job runs
  on, such as `ubuntu-latest`, `windows-latest`, or `macos-latest`, each corresponding to an environment with the
  respective
  OS installed.
* `uses`: This declaration specifies external extensions that are used in the workflow. External extensions can be
  actions, or other workflows that are stored in a different repository. A catalogue of external extensions can be found
* `needs`: This declaration specifies the dependencies between jobs. If a job depends on another job, the dependent job
  will only run if the job it depends on is successful.
* `working-directory`: This declaration specifies the working directory of the job. This is useful when you want to run
  the job in a different directory from the default working directory.
* `run`: This declaration specifies the shell commands that are run in the step. The shell commands are run in the
  environment specified by the `runs-on` declaration.

Refer to
the [documentation by GitHub](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
for more information on the different GitHub Actions workflow syntaxes that are available.

To better understand the workflows that are used in the Sample Application, refer to the YML files under the
[`.github/workflows`](../../.github/workflows) directory and the CI/CD documentation under the
[Developer Guide](Developer%20Guide.md#cicd).

### Preparation

> [!WARNING]
> Make sure to complete the preparation steps under the AWS and Codecov section before proceeding with the steps below!

Before you can deploy the application to AWS, you need to set up GitHub Actions.

Follow [this guide](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions) to add the
following GitHub Actions Secrets to the repository:

1. `AWS_ACCESS_KEY_ID`: The Access Key ID of the IAM user that you created in the AWS preparation step.
2. `AWS_SECRET_ACCESS_KEY`: The Secret Access Key of the IAM user that you created in the AWS preparation step.
3. `AWS_REGION`: The AWS region that you want to deploy the application to. This should correspond to the region that
   is used under the [`deploy` directory](../deploy).
4. `CODECOV_TOKEN`: The Repository Upload Token that you obtained from Codecov.

## Docker

Docker is a containerisation tool and framework to help you ship applications consistently and reliably.

Docker is the main tool used for deployment as it helps to ensure that the sample application can be quickly deployed
and torn down predictably and consistently.

### Images and Dockerfiles

Docker **Images** are the building blocks of Docker containers. A Docker image is a lightweight, standalone,
executable package of software that includes everything needed to run a piece of software, including the code,
runtime and dependencies.

A **Dockerfile** is a text file that contains a set of instructions that are used to create a Docker image.

For the Sample Application, the Dockerfile used to create a container containing the Sample Application is found
at the top level application directory [here](../app/Dockerfile).

Most crucially, a Dockerfile should contain the following clauses:

```dockerfile
FROM ...
WORKDIR ...
EXPOSE ...
COPY ...
RUN ...
```

* `FROM`: The base image that the Docker image is built on.
* `WORKDIR`: The working directory of the Docker container. This should mirror the name of the folder that the
  application code is stored in.
* `EXPOSE`: The port that is exposed (accessible) from outside the container. This depends on the port that you set in
  your [Streamlit configuration file](../app/.streamlit/config.toml). By default, the port is `8502`.
* `COPY`: Copies the application code from your device into the Docker container.
* `RUN`: This clause is used to specify a command that is executed when the container is started.

A completed Dockerfile with minimal configurations required to run the application should look like this:

```dockerfilesp
FROM python:3.12
WORKDIR /app
EXPOSE 80

COPY .. .

RUN pip install --no-cache-dir -r requirements.txt
```

This is the Dockerfile that is used to build the Docker image for the Sample Application.

### Docker Commands

There are only 2 main commands which you need to be aware of when using Docker:

1. `docker build`: This command is used to build a Docker image from a Dockerfile.
2. `docker run`: This command is used to run a Docker container from a Docker image.

#### `docker build`

To build a Docker image from a Dockerfile, you can run the following command:

```shell
docker build -t [IMAGE_NAME] .
```

This command builds a Docker image from the Dockerfile in the current directory and tags the image with the specified
image name.

> [!NOTE]
> Images are usually tagged with a version number to indicate the version of the image. For example, `my-image:1.0.0` or
> `my-image:latest`, where `my-image` is the name of the image and `1.0.0` and `latest` are the version numbers.

> [!WARNING]
> Replace `[IMAGE_NAME]` in whole with the name of the Docker image that you want to build.

> [!CAUTION]
> Make sure that the Docker daemon is active and running before running the `docker build` command. Failure to do so may
> result in errors!

#### `docker run`

To run a Docker container from a Docker image, you can run the following command:

```shell
docker run -p [HOST_PORT]:[CONTAINER_PORT] [IMAGE_NAME]
```

This command runs a Docker container from the specified Docker image and maps the host port to the container port.

> [!NOTE]
> The host port is the port that is exposed on the host machine, while the container port is the port that is exposed
> in the Docker container.

> [!WARNING]
> Replace `[HOST_PORT]`, `[CONTAINER_PORT]` and `[IMAGE_NAME]` in whole with the host port, container port and image
> name as specified above in `docker build` respectively.

> [!CAUTION]
> Make sure that the Docker daemon is active and running before running the `docker run` command. Failure to do so may
> result in errors!

## Terraform

Terraform is an open-source infrastructure as code tool that allows you to define and provision infrastructure using a
high-level configuration language.

Terraform allows you to define the infrastructure that you want to create in configuration files, and then use the
Terraform CLI to create, update, and destroy the infrastructure.

Terraform is used in the deployment of the Sample Application to create the necessary infrastructure in AWS to host the
application. In particular, Terraform is used in conjunction with GitHub Actions to automatically provision the
necessary resources and configure the provisioned resources.


> [!NOTE]
> Refer to the GitHub Actions [workflow file](../../.github/workflows/integration.yml) to see how Terraform is used in
> conjunction with GitHub Actions to deploy the Sample Application.

### Install Terraform

To install the Terraform CLI on your machine, follow the instructions provided in
the [official Terraform documentation](https://developer.hashicorp.com/terraform/install).

> [!NOTE]
> This step is not necessary as GitHub Actions can be used to run Terraform commands in an environment that is already
> configured for you.

### Organisation of Terraform Code

The Terraform code for the Sample Application is organised into two main directories: `create-backend` and
`main-infrastructure`.

The `create-backend` directory contains the Terraform code that is used to provision the S3 bucket and DynamoDB table
that is used to store the Terraform state and lock the state respectively.

The `main-infrastructure` directory contains the Terraform code that is used to provision the main infrastructure of the
Sample Application, such as the VPC, subnets, security groups, and other resources that are required to host the
application.

#### `create-backend`

Terraform allows you to save the state of your infrastructure in a remote backend, such as an Amazon S3 bucket, and use
NoSQL databases like Amazon DynamoDB to lock the state to prevent concurrent modifications.

For the Sample Application, we will deploy the S3 bucket and DynamoDB table to store the Terraform state and lock the
state respectively.

The Terraform code used to provision these resources can be found in the [`create-backend`](../deploy/create-backend)
directory.


> [!CAUTION]
> If you are deploying the application locally rather than via GitHub Actions, make sure to initialise the Terraform
> code within this folder before attempting to initialise the main infrastructure.
>
> Failure to do so may result in the deployment of the main infrastructure to fail!

#### `main-infrastructure`

> [!CAUTION]
> Make sure to initialise the necessary AWS resources under `create-backend` first, before initialising the main
> infrastructure contained in this directory!

This directory contains the Terraform code that is used to deploy the main infrastructure of the Sample Application to
AWS.

You may freely change and edit the Terraform code to suit your needs, but make sure to test the changes before
deploying them to production!

More information on the overall architecture of the Sample Application can be found below under
[Cloud Architecture](#cloud-architecture).

> [!TIP]
> Terraform does not care about how you structure your code within the same directory. You can split your code into
> multiple files and Terraform will treat them as a single configuration!
>
> For the Sample Application, we have split the Terraform code into multiple files to make it easier to manage and
> maintain the different components of the Sample Application!

### Terraform Configuration

Before you can use Terraform to deploy the Sample Application, you will need to initialise Terraform and retrieve the
required backend configurations.

To do so, you need to run the following command in the directories contained within the `deploy/` directory:

```shell
terraform init
```

Each directory contains the necessary Terraform code needed to deploy component(s) of the Sample Application to AWS.

> [!TIP]
> If you have already done this step previously and are repeating it, you can run the Terraform command with
> the `-reconfigure` flag to force Terraform to reconfigure the backend configurations!

### Terraform Modules

Terraform modules are reusable, composable units of Terraform configuration that are used to define a set of resources.

Terraform modules are used in the deployment process to store global configuration variables used throughout the
process.

The constants can be found under the `deploy/modules/constants/` directory in
the [`constants.tf`](../deploy/modules/constants/constants.tf) file.

### Terraform Plan

After initialising Terraform, you can run the following command to generate a Terraform plan:

```shell
terraform plan
```

This command will generate a plan that shows you what Terraform will do when you apply the configuration.

> [!NOTE]
> This step is not necessary if you are sure that your infrastructure is correctly configured or if you are
> redeploying/verifying the infrastructure (due to a change in the code which triggers a GitHub Actions workflow
> or otherwise).

### Terraform Apply

After generating the Terraform plan, you can run the following command to apply the configuration:

```shell
terraform apply
```

This command will apply the configuration and create the necessary infrastructure in AWS.

### Terraform Destroy

If you want to destroy the infrastructure that you have created, you can run the following command:

```shell
terraform destroy
```

## Cloud Architecture

Now that you understand the main tools that we will be using in the deployment of the Sample Application to AWS,
let's next take a look at the AWS architecture that is used to serve the application.

### Services

Let's take a look at the services that we will be using in the application.

1. **Amazon Virtual Private Cloud (VPC)**: VPC is a service that lets you launch AWS resources in a virtual network that
   you define. You have complete control over your virtual networking environment, including selection of your IP
   address range, creation of subnets, and configuration of route tables and network gateways.
2. **Subnets**: Subnets are segments of a VPC's IP address range that you can use to group resources based on security
   and operational needs.
3. **Amazon Elastic Compute Cloud (EC2)**: EC2 is a web service that provides secure, resizable compute capacity in the
   cloud. It is designed to make web-scale cloud computing easier for developers.
4. **Amazon Elastic Container Service (ECS)**: ECS is a fully managed container orchestration service that allows you to
   easily run, stop, and manage Docker containers on a cluster.
5. **Amazon Elastic Container Registry (ECR)**: ECR is a fully managed Docker container registry that makes it easy for
   developers to store, manage, and deploy Docker container images.
6. **Amazon Fargate**: Fargate is a serverless compute engine for containers that works with both ECS and EKS. Fargate
   removes the need to provision and manage servers, lets you specify and pay for resources per application, and
   improves security through application isolation by design.
   **This is a planned enhancement to the Sample Application.**
7. **Amazon Application Load Balancer (ALB)**: ALB is a load balancer that operates at the application layer and allows
   you to define routing rules based on content across multiple services or containers running on one or more EC2
   instances.
8. **Amazon CloudWatch**: CloudWatch is a monitoring and observability service built for DevOps engineers, developers,
   site reliability engineers (SREs), and IT managers. CloudWatch provides you with data and actionable insights to
   monitor your applications, respond to system-wide performance changes, optimize resource utilization, and get a
   unified view of operational health.
9. **Amazon Simple Storage Service (S3)**: S3 is an object storage service that offers industry-leading scalability,
   data availability, security, and performance. S3 is designed for 99.999999999% (11 9's) of durability, and stores
   data for millions of applications for companies all around the world.
10. **Amazon DynamoDB**: DynamoDB is a key-value and document database that delivers single-digit millisecond
    performance at any scale. It's a fully managed, multi-region, multi-master database with built-in security, backup
    and restore, and in-memory caching for internet-scale applications.

Let's zoom into the few services that we will actively be using and managing in the application.

#### EC2

EC2 is used to provide the application with a platform and compute capabilities to run on.

In the initial stages of deployment, this was used as it allows you to get the application up and running quickly, by
provisioning an EC2 instance on-demand and manually deploying the application on it without many configurations required
by the developer.

However, as we move towards a more cloud-native solution, we will be using ECS in conjunction with Fargate to manage the
orchestration and deployment of the application through Docker containers instead, rather than using bare EC2 instances
to host the application.

#### ECR

ECR is a scalable private container registry (something like GitHub for Docker images!) that allows you to store,
manage, and deploy Docker container images.

ECR has integrations with ECS that allow you to easily push and pull Docker images from the registry to the ECS, and
trigger upstream changes to ECS services when a new image is pushed to the registry.

This allows you to create complex Continuous Deployment pipelines that automatically deploy new versions of the
production application when a new image is ready.

#### ECS

ECS is used to orchestrate and manage the deployment of the application through Docker containers.

ECS allows you to define a task definition that specifies the Docker container image to use, the CPU and memory
requirements, the networking configuration, and other configurations that are required to run the application.

ECS also allows you to define a service that manages the task definition and ensures that the application is running
according to the configurations specified in the task definition.

You will be using this service mostly throughout the deployment process.

#### Fargate

> [!NOTE]
> Fargate is a planned enhancement to the Sample Application!

Fargate is a serverless compute engine for containers that allows you to run containers without having to manage the
underlying infrastructure.

Fargate allows you to specify the CPU and memory requirements of the application, and AWS will automatically provision
the necessary resources to run the application.

This allows you to focus on the application itself, rather than the underlying infrastructure that the application is
running on.

This is especially useful for the Sample Application since the infrastructural security of the application can be
managed by AWS instead, offloading the responsibility of keeping our system updated and patched to AWS.

#### Elastic Load Balancer

The Elastic Load Balancer (ELB) is a service that automatically distributes incoming application traffic across
multiple targets, such as EC2 instances, containers, and IP addresses.

ELB is used to distribute incoming traffic across multiple instances of the application to ensure that the application
is highly available and fault-tolerant.

ELB is used to route traffic to the application and to ensure that the application is running and healthy.

### Production Architecture

The following architectural diagram shows the AWS, GitHub and Terraform services that are used in the deployment of the
Sample Application:

![infrastructure diagram](assets/deployment-guide/Infrastructure.png)

The diagram also shows the workflows between the different services, and how they interact with each other to deploy the
Sample Application to AWS.

This architecture is implemented within the Terraform code.

You can also notice that there is a distinct split in the processes needed to deploy the application, with the
`create-backend` directory handling the creation of the S3 bucket and DynamoDB table, and the `main-infrastructure`
directory handling the creation of the main infrastructure of the Sample Application. GitHub and Terraform are also
involved in the deployment process, with GitHub Actions being used to test and deploy the application, and Terraform
being used as an infrastructure as a code tool to automatically check the status of AWS resources and deploy the
application.

The following is a rough process of what happens when you deploy the application to AWS:

1. On a push to the repository, GitHub Actions is triggered.
2. GitHub Actions trigger unit tests, linting and code coverage checks.
3. GitHub Actions then uses Terraform to check the status of the Terraform remote backend, provisioning the resources
   as needed if it is missing in the target AWS environment
4. GitHub Actions finally uses Terraform to check the status of the main infrastructure and provision resources if it
   is missing in the AWS environment or if Terraform files have changed
5. For networking,
    1. A VPC, its associated public and private Subnets, public and private Route Tables, Internet Gateway, NAT Gateway,
       Elastic IP and Security Groups are created.
    2. An Application Load Balancer is created to route traffic to the ECS Service
6. For ECS,
    1. A private ECR Repository is created to store Docker images of the Sample Application
    2. An ECS Service, ECS Cluster, Capacity Provider, Task Definition and EC2 Launch Templates are then created, along
       with the associated ECS and EC2 Roles and Policies
7. For compute (EC2),
    1. An Auto Scaling Group and EC2 Container Instances are created
    2. The ECS Service is then linked to the Auto Scaling Group to ensure that the ECS Service is running on the EC2
       Container Instances through the Capacity Provider
