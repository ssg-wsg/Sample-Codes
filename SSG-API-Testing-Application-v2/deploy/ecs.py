"""
IaC template for uploading task definitions and creating/updating a service in ECS.

Inspired from https://aws.plainenglish.io/creating-vpc-using-boto3-terraform-cloudformation-and-both-af741a8afb3c
"""

import os
import boto3
import logging

from prettytable import PrettyTable
from botocore.config import Config

from constants import ECS_TASK_DEFINITION_FAMILY, ECS_SERVICE_NAME, ECS_TASK_MEMORY, ECS_TASK_CPU, \
    CONTAINER_APPLICATION_PORT, ECS_CONTAINER_NAME, AWS_REGION, ECS_CLUSTER_NAME


class ECS:
    """
    Class that helps to set up ECS with the correct task definition.
    """

    # create a logger
    LOGGER = logging.getLogger("infrastructure-provisioning")

    # set up stream handler with correct logging level and format
    FORMATTER = logging.Formatter("%(asctime)s - %(name)s - %(levelname)-9s - %(message)s")
    STREAM_HANDLER = logging.StreamHandler()
    STREAM_HANDLER.setLevel(logging.INFO)
    STREAM_HANDLER.setFormatter(FORMATTER)

    # set up logger with correct logging level and add stream handler
    LOGGER.setLevel(logging.INFO)
    LOGGER.addHandler(STREAM_HANDLER)

    # set up AWS client config
    CONFIG = Config(
        region_name=AWS_REGION  # CHANGE THIS TO YOUR REGION OF CHOICE
    )

    def __init__(self):
        # define exportable variables
        self.ecs_task_definition_arn: str = None

        # define clients and resources
        self.ecs = boto3.client("ecs", config=ECS.CONFIG)

        # call setup methods and export exportable variables to env file if it exists
        ECS._assert_env()
        self._setup()
        self._export_to_env()
        self._log_env_vars()

    @staticmethod
    def _assert_env():
        if os.getenv("ECS_CLUSTER_ARN") is None:
            raise AssertionError("Missing ECS_CLUSTER_ARN environment variable!")

        if os.getenv("SUBNET_ID_1") is None:
            raise AssertionError("Missing SUBNET_ID_1 environment variable!")

        if os.getenv("SUBNET_ID_2") is None:
            raise AssertionError("Missing SUBNET_ID_2 environment variable!")

        if os.getenv("SUBNET_ID_3") is None:
            raise AssertionError("Missing SUBNET_ID_3 environment variable!")

        if os.getenv("SECURITY_GROUP_ID") is None:
            raise AssertionError("Missing SECURITY_GROUP_ID environment variable!")

        if os.getenv("ECS_IMAGE") is None:
            raise AssertionError("Missing ECS_IMAGE environment variable!")

    def _setup(self):
        """Calls the setup methods in the correct order to provision the infrastructure."""

        self._create_task_definition()
        self._create_or_update_service()

    def _export_to_env(self):
        ECS.LOGGER.info("Writing environment variables to GitHub Actions environment file...")

        # taken from
        # https://stackoverflow.com/questions/70123328/how-to-set-environment-variables-in-github-actions-using-python
        env_file = os.getenv("GITHUB_ENV")

        if env_file is None:
            os.putenv("ECS_TASK_DEFINITION_ARN", self.ecs_task_definition_arn)

        with open(env_file, "a") as f:
            f.write(f"ECS_TASK_DEFINITION_ARN={self.ecs_task_definition_arn}\n")

        ECS.LOGGER.info("Environment variables written to GitHub Actions environment file successfully!")

    def _log_env_vars(self):
        tabulated = PrettyTable(field_names=["Variable", "Value"])
        tabulated.add_row(["ECS Task Definition ARN", self.ecs_task_definition_arn])

        print(tabulated)

    def _create_task_definition(self):
        ECS.LOGGER.info("Creating task definition...")

        task_definition = self.ecs.register_task_definition(
            family=ECS_TASK_DEFINITION_FAMILY,
            networkMode="awsvpc",
            containerDefinitions=[
                {
                    "memory": ECS_TASK_MEMORY,
                    "cpu": ECS_TASK_CPU,
                    "name": ECS_CONTAINER_NAME,
                    "image": os.getenv("ECS_IMAGE"),
                    "portMappings": [
                        {
                            "containerPort": CONTAINER_APPLICATION_PORT,
                            "hostPort": CONTAINER_APPLICATION_PORT,
                            "protocol": "tcp",
                            "appProtocol": "http"
                        }
                    ],
                    "healthCheck": {
                        "command": ["CMD-SHELL", "curl -f http://localhost:8502/ || exit 1"],
                        "interval": 60,
                        "timeout": 15,
                        "retries": 3
                    },
                    "essential": True,
                    "disableNetworking": False,
                    "privileged": True,
                    "readonlyRootFilesystem": False,
                    "interactive": True,
                    "pseudoTerminal": True
                }
            ],
            requiresCompatibilities=[
                "EC2"
            ],
            runtimePlatform={
                "cpuArchitecture": "X86_64",
                "operatingSystemFamily": "LINUX"
            }
        )

        self.ecs_task_definition_arn = task_definition['taskDefinition']['taskDefinitionArn']
        ECS.LOGGER.info(f"Task definition created successfully! Task Definition ARN: {self.ecs_task_definition_arn}")

    def _create_or_update_service(self):
        svcs = self.ecs.describe_services(
            cluster=ECS_CLUSTER_NAME,
            services=[
                ECS_SERVICE_NAME
            ]
        )

        if len(svcs["services"]) > 0:
            # service exists, so we update it instead
            ECS.LOGGER.warning(f"ECS service with name {ECS_SERVICE_NAME} already exists! Updating existing service...")
            self.ecs.update_service(
                taskDefinition=self.ecs_task_definition_arn,
            )
        else:
            ECS.LOGGER.info("Creating ECS service...")
            create_service = self.ecs.create_service(
                cluster=ECS_CLUSTER_NAME,
                serviceName=ECS_SERVICE_NAME,
                taskDefinition=self.ecs_task_definition_arn,
                desiredCount=1,
                launchType="EC2",
                networkConfiguration={
                    "awsvpcConfiguration": {
                        "subnets": [
                            os.getenv("SUBNET_ID_1"),
                            os.getenv("SUBNET_ID_2"),
                            os.getenv("SUBNET_ID_3")
                        ],
                        "securityGroups": [
                            os.getenv("SECURITY_GROUP_ID")
                        ],
                    }
                },
                schedulingStrategy="REPLICA",
                deploymentController={
                    "type": "ECS"
                },
            )
            ECS.LOGGER.info(f"Service created successfully! Service ARN: {create_service['service']['serviceArn']}")


if __name__ == '__main__':
    ECS()
