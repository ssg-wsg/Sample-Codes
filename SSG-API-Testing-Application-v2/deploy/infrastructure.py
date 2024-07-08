"""
IaC template for creating base cloud environment

Inspired from https://aws.plainenglish.io/creating-vpc-using-boto3-terraform-cloudformation-and-both-af741a8afb3c
"""
import base64
import json
import os
import time

import boto3
import logging

from botocore.exceptions import ClientError
from prettytable import PrettyTable

from constants import (CIDR_BLOCK, SUBNET_CIDR_ONE, SUBNET_CIDR_TWO, SUBNET_CIDR_THREE, ECS_CLUSTER_NAME, ECS_IMAGE_AMI,
                       ECS_LAUNCH_TEMPLATE_NAME, ECS_ASG_NAME, ECS_CAPACITY_PROVIDER_NAME, ECR_REPO_NAME,
                       SG_GROUP_NAME, CONTAINER_APPLICATION_PORT, AWS_REGION, INSTANCE_PROFILE_NAME)
from botocore.config import Config


class Infrastructure:
    """
    Class that helps to set up the cloud architecture.
    """

    # create a logger
    LOGGER = logging.getLogger("infrastructure-provisioning")

    # set up stream handler with correct logging level and format
    FORMATTER = logging.Formatter("%(asctime)s - %(levelname)-8s - %(message)s")
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
        self.vpc_id: str = None
        self.igw_id: str = None
        self.rt_id: str = None
        self.subnet_id_1: str = None
        self.subnet_id_2: str = None
        self.subnet_id_3: str = None
        self.sg_id: str = None
        self.instance_profile_arn: str = None
        self.asg_arn: str = None
        self.ecs_cluster_arn: str = None
        self.ecs_launch_template_id: str = None

        # define clients and resources
        self.table = None  # type: boto3.resource("ec2").RouteTable
        self.ec2 = boto3.client("ec2", config=Infrastructure.CONFIG)
        self.asg = boto3.client("autoscaling", config=Infrastructure.CONFIG)
        self.ecr = boto3.client("ecr", config=Infrastructure.CONFIG)
        self.ecs = boto3.client("ecs", config=Infrastructure.CONFIG)
        self.iam = boto3.client("iam", config=Infrastructure.CONFIG)

        # call setup methods and export exportable variables to env file if it exists
        self._setup()
        self._export_to_env()
        self._log_env_vars()

    def _setup(self):
        """Calls the setup methods in the correct order to provision the infrastructure."""

        self._create_or_reuse_vpc()
        self._enable_public_dns()
        self._create_or_reuse_internet_gateway()
        self._create_or_reuse_routing_table()
        self._create_or_reuse_subnets()
        self._associate_subnets_with_routing_table()
        self._create_or_reuse_security_groups()
        self._setup_role()
        self._create_or_reuse_launch_template()
        self._create_or_reuse_auto_scaling_group()
        self._create_or_reuse_ecr_repo()
        self._create_or_reuse_capacity_provider()
        self._create_or_reuse_ecs_cluster()

    def _export_to_env(self):
        Infrastructure.LOGGER.info("Writing environment variables to GitHub Actions environment file...")

        # taken from
        # https://stackoverflow.com/questions/70123328/how-to-set-environment-variables-in-github-actions-using-python
        env_file = os.getenv("GITHUB_ENV")

        if env_file is None:
            os.putenv("VPC_ID", self.vpc_id)
            os.putenv("IGW_ID", self.igw_id)
            os.putenv("RT_ID", self.rt_id)
            os.putenv("SUBNET_ID_1", self.subnet_id_1)
            os.putenv("SUBNET_ID_2", self.subnet_id_2)
            os.putenv("SUBNET_ID_3", self.subnet_id_3)
            os.putenv("INSTANCE_PROFILE_ARN", self.instance_profile_arn)
            os.putenv("SECURITY_GROUP_ID", self.sg_id)
            os.putenv("ASG_ARN", self.asg_arn)
            os.putenv("ECS_CLUSTER_ARN", self.ecs_cluster_arn)
            os.putenv("ECS_LAUNCH_TEMPLATE_ID", self.ecs_launch_template_id)

        with open(env_file, "a") as f:
            f.write(f"VPC_ID={self.vpc_id}\n")
            f.write(f"IGW_ID={self.igw_id}\n")
            f.write(f"RT_ID={self.rt_id}\n")
            f.write(f"SUBNET_ID_1={self.subnet_id_1}\n")
            f.write(f"SUBNET_ID_2={self.subnet_id_2}\n")
            f.write(f"SUBNET_ID_3={self.subnet_id_3}\n")
            f.write(f"INSTANCE_PROFILE_ARN={self.instance_profile_arn}\n")
            f.write(f"SECURITY_GROUP_ID={self.sg_id}\n")
            f.write(f"ASG_ARN={self.asg_arn}\n")
            f.write(f"ECS_CLUSTER_ARN={self.ecs_cluster_arn}\n")
            f.write(f"ECS_LAUNCH_TEMPLATE_ID={self.ecs_launch_template_id}\n")

        Infrastructure.LOGGER.info("Environment variables written to GitHub Actions environment file successfully!")

    def _log_env_vars(self):
        tabulated = PrettyTable(field_names=["Variable", "Value"])
        tabulated.add_row(["VPC ID", self.vpc_id])
        tabulated.add_row(["Internet Gateway ID", self.igw_id])
        tabulated.add_row(["Routing Table ID", self.rt_id])
        tabulated.add_row(["Subnet 1 ID", self.subnet_id_1])
        tabulated.add_row(["Subnet 2 ID", self.subnet_id_2])
        tabulated.add_row(["Subnet 3 ID", self.subnet_id_3])
        tabulated.add_row(["Instance Profile ARN", self.instance_profile_arn])
        tabulated.add_row(["Security Group ID", self.sg_id])
        tabulated.add_row(["Auto-Scaling Group ARN", self.asg_arn])
        tabulated.add_row(["ECS Cluster ARN", self.ecs_cluster_arn])
        tabulated.add_row(["ECS Launch Template ID", self.ecs_launch_template_id])

        print(tabulated)

    def _create_or_reuse_vpc(self):
        # check if the VPC already exists
        vpcs = self.ec2.describe_vpcs(
            Filters=[
                {
                    "Name": "cidr",
                    "Values": [
                        CIDR_BLOCK
                    ]
                }
            ]
        )

        if len(vpcs["Vpcs"]) > 0:
            Infrastructure.LOGGER.warning(f"VPC with CIDR block {CIDR_BLOCK} already exists! Reusing existing VPC...")
            self.vpc_id = vpcs["Vpcs"][0]["VpcId"]
        else:
            Infrastructure.LOGGER.info("Creating VPC...")
            vpc = self.ec2.create_vpc(
                CidrBlock=CIDR_BLOCK
            )
            self.vpc_id = vpc["Vpc"]["VpcId"]
            Infrastructure.LOGGER.info(f"VPC created successfully! VPC ID: {self.vpc_id}")

    def _enable_public_dns(self):
        # enable public DNS hostname for SSH
        Infrastructure.LOGGER.info("Enabling public DNS hostname for VPC...")
        self.ec2.modify_vpc_attribute(
            VpcId=self.vpc_id, EnableDnsSupport={"Value": True}
        )
        self.ec2.modify_vpc_attribute(
            VpcId=self.vpc_id, EnableDnsHostnames={"Value": True}
        )
        Infrastructure.LOGGER.info("Public DNS hostname for VPC enabled successfully!")

    def _create_or_reuse_internet_gateway(self):
        # check if the internet gateway already exists
        igws = self.ec2.describe_internet_gateways(
            Filters=[
                {
                    "Name": "attachment.vpc-id",
                    "Values": [
                        self.vpc_id
                    ]
                }
            ]
        )

        if len(igws["InternetGateways"]) > 0:
            Infrastructure.LOGGER.warning("Internet Gateway already exists! Skipping creation...")
            self.igw_id = igws["InternetGateways"][0]["InternetGatewayId"]
        else:
            # create internet gateway
            Infrastructure.LOGGER.info("Creating internet gateway...")
            ig = self.ec2.create_internet_gateway()
            self.igw_id = ig["InternetGateway"]["InternetGatewayId"]
            Infrastructure.LOGGER.info(
                f"Internet gateway created successfully! Internet Gateway ID: {self.igw_id}")

            # attach newly created internet gateway to VPC
            Infrastructure.LOGGER.info("Attaching IGW to VPC...")
            self.ec2.attach_internet_gateway(
                VpcId=self.vpc_id,
                InternetGatewayId=ig["InternetGateway"]["InternetGatewayId"]
            )
            Infrastructure.LOGGER.info("IGW attached to VPC successfully!")

    def _create_or_reuse_routing_table(self):
        rts = self.ec2.describe_route_tables(
            Filters=[
                {
                    "Name": "vpc-id",
                    "Values": [
                        self.vpc_id
                    ]
                }
            ]
        )

        if len(rts["RouteTables"]) > 0:
            Infrastructure.LOGGER.warning("Routing table already exists! Skipping creation...")
            self.rt_id = rts["RouteTables"][0]["RouteTableId"]

            # check if the required rote is present
            routes = self.ec2.describe_route_tables(
                RouteTableIds=[
                    self.rt_id
                ]
            )["RouteTables"][0]["Routes"]

            if not any(map(lambda x: (
                    x["DestinationCidrBlock"] == "0.0.0.0/0"
                    and x["GatewayId"] == self.igw_id), routes)):
                Infrastructure.LOGGER.warning("Missing route to internet gateway! Creating route...")
                self.ec2.create_route(
                    DestinationCidrBlock="0.0.0.0/0",
                    GatewayId=self.igw_id,
                    RouteTableId=self.rt_id
                )
                Infrastructure.LOGGER.info("Route to internet gateway created successfully!")
        else:
            # create a routing table
            Infrastructure.LOGGER.info("Creating routing table...")
            rt = self.ec2.create_route_table(VpcId=self.vpc_id)
            self.rt_id = rt["RouteTable"]["RouteTableId"]
            Infrastructure.LOGGER.info(f"Routing table created successfully! Route Table ID: {self.rt_id}")

            # create a route to the internet gateway
            Infrastructure.LOGGER.info("Creating route to internet gateway...")
            self.ec2.create_route(
                DestinationCidrBlock="0.0.0.0/0",
                GatewayId=self.igw_id,
                RouteTableId=self.rt_id
            )
            Infrastructure.LOGGER.info("Route to internet gateway created successfully!")

    def _create_or_reuse_subnets(self):
        subnets = self.ec2.describe_subnets(
            Filters=[
                {
                    "Name": "vpc-id",
                    "Values": [
                        self.vpc_id
                    ]
                }
            ]
        )["Subnets"]

        subnets_cidrs = [subnet["CidrBlock"] for subnet in subnets]

        if SUBNET_CIDR_ONE not in subnets_cidrs:
            Infrastructure.LOGGER.info("Creating subnets and associating them with the routing table...")
            subnet1 = self.ec2.create_subnet(
                AvailabilityZone="ap-southeast-1a",
                CidrBlock=SUBNET_CIDR_ONE,
                VpcId=self.vpc_id
            )
            self.ec2.modify_subnet_attribute(
                MapPublicIpOnLaunch={
                    'Value': True
                },
                SubnetId=subnet1["Subnet"]["SubnetId"]
            )
            self.subnet_id_1 = subnet1["Subnet"]["SubnetId"]
            Infrastructure.LOGGER.info(f"Subnet 1 created successfully! Subnet ID: {self.subnet_id_1}")
        else:
            Infrastructure.LOGGER.warning("Subnet 1 already exists! Skipping creation...")
            # safe as we have ascertained that the subnet exists with the check above
            self.subnet_id_1 = (
                list(map(lambda y: y["SubnetId"], filter(lambda x: x["CidrBlock"] == SUBNET_CIDR_ONE, subnets)))[0])

        if SUBNET_CIDR_TWO not in subnets_cidrs:
            subnet2 = self.ec2.create_subnet(
                AvailabilityZone="ap-southeast-1b",
                CidrBlock=SUBNET_CIDR_TWO,
                VpcId=self.vpc_id
            )
            self.ec2.modify_subnet_attribute(
                MapPublicIpOnLaunch={
                    'Value': True
                },
                SubnetId=subnet2["Subnet"]["SubnetId"]
            )
            self.subnet_id_2 = subnet2["Subnet"]["SubnetId"]
            Infrastructure.LOGGER.info(f"Subnet 2 created successfully! Subnet ID: {self.subnet_id_2}")
        else:
            Infrastructure.LOGGER.warning("Subnet 2 already exists! Skipping creation...")
            # safe as we have ascertained that the subnet exists with the check above
            self.subnet_id_2 = (
                list(map(lambda y: y["SubnetId"], filter(lambda x: x["CidrBlock"] == SUBNET_CIDR_TWO, subnets)))[0]
            )

        if SUBNET_CIDR_THREE not in subnets_cidrs:
            subnet3 = self.ec2.create_subnet(
                AvailabilityZone="ap-southeast-1c",
                CidrBlock=SUBNET_CIDR_THREE,
                VpcId=self.vpc_id
            )
            self.ec2.modify_subnet_attribute(
                MapPublicIpOnLaunch={
                    'Value': True
                },
                SubnetId=subnet3["Subnet"]["SubnetId"]
            )
            self.subnet_id_3 = subnet3["Subnet"]["SubnetId"]
            Infrastructure.LOGGER.info(f"Subnet 3 created successfully! Subnet ID: {self.subnet_id_3}")
        else:
            Infrastructure.LOGGER.warning("Subnet 3 already exists! Skipping creation...")
            # safe as we have ascertained that the subnet exists with the check above
            self.subnet_id_3 = (
                list(map(lambda y: y["SubnetId"], filter(lambda x: x["CidrBlock"] == SUBNET_CIDR_THREE, subnets)))[0]
            )

    def _associate_subnets_with_routing_table(self):
        self.table = boto3.resource("ec2", config=Infrastructure.CONFIG).RouteTable(self.rt_id)

        routes = self.ec2.describe_route_tables(
            Filters=[
                {
                    "Name": "vpc-id",
                    "Values": [
                        self.vpc_id
                    ]
                }
            ]
        )

        Infrastructure.LOGGER.info("Associating routing table with Subnet 1...")
        self.table.associate_with_subnet(SubnetId=self.subnet_id_1)

        Infrastructure.LOGGER.info("Associating routing table with Subnet 2...")
        self.table.associate_with_subnet(SubnetId=self.subnet_id_2)

        Infrastructure.LOGGER.info("Associating routing table with Subnet 3...")
        self.table.associate_with_subnet(SubnetId=self.subnet_id_3)

    def _create_or_reuse_security_groups(self):
        # check if the required SG already exists, and if so, retrieve it
        sgs = self.ec2.describe_security_groups(
            Filters=[
                {
                    "Name": "vpc-id",
                    "Values": [
                        self.vpc_id
                    ]
                },
                {
                    "Name": "group-name",
                    "Values": [
                        SG_GROUP_NAME
                    ]
                }
            ]
        )

        if len(sgs["SecurityGroups"]) > 0:
            Infrastructure.LOGGER.warning("Security group already exists! Skipping creation...")
            self.sg_id = sgs["SecurityGroups"][0]["GroupId"]

            ip_perms = sgs["SecurityGroups"][0]["IpPermissions"]

            if not (
                    any(map(lambda x: (
                            x["FromPort"] == 80
                            and x["ToPort"] == CONTAINER_APPLICATION_PORT
                            and (len(x["IpRanges"]) > 0 and x["IpRanges"][0]["CidrIp"] == "0.0.0.0/0")
                    ), ip_perms))
                    and any(map(lambda x: (
                    x["FromPort"] == 433
                    and x["ToPort"] == CONTAINER_APPLICATION_PORT
                    and (len(x["IpRanges"]) > 0 and x["IpRanges"][0]["CidrIp"] == "0.0.0.0/0")), ip_perms))
            ):
                Infrastructure.LOGGER.warning("Security group ingress rules not authorized! Authorizing...")
                self.ec2.authorize_security_group_ingress(
                    GroupId=self.sg_id,
                    IpPermissions=[
                        {
                            "FromPort": 80,
                            "ToPort": CONTAINER_APPLICATION_PORT,  # THIS MUST BE CHANGED TO THE CORRECT PORT NUMBER
                            "IpProtocol": "tcp",
                            "IpRanges": [
                                {
                                    "CidrIp": "0.0.0.0/0",
                                    "Description": "Allow HTTP traffic from anywhere"
                                }
                            ],
                            "Ipv6Ranges": [],
                            "PrefixListIds": [],
                            "UserIdGroupPairs": []
                        },
                        {
                            "FromPort": 433,
                            "ToPort": CONTAINER_APPLICATION_PORT,  # THIS MUST BE CHANGED TO THE CORRECT PORT NUMBER
                            "IpProtocol": "tcp",
                            "IpRanges": [
                                {
                                    "CidrIp": "0.0.0.0/0",
                                    "Description": "Allow HTTPS traffic from anywhere"
                                }
                            ],
                            "Ipv6Ranges": [],
                            "PrefixListIds": [],
                            "UserIdGroupPairs": []
                        }
                    ]
                )
                Infrastructure.LOGGER.info("Security group ingress rules authorized successfully!")
        else:
            Infrastructure.LOGGER.info("Creating security group...")
            sg = self.ec2.create_security_group(
                Description="Security group for SSG-WSG Sample Application",
                GroupName=SG_GROUP_NAME,
                VpcId=self.vpc_id  # CHANGE THIS TO YOUR VPC ID IN THE REGION
            )
            self.sg_id = sg["GroupId"]
            Infrastructure.LOGGER.info(f"Security group created successfully! Security Group ID: {self.sg_id}")

            Infrastructure.LOGGER.info("Authorizing security group ingress rules...")
            self.ec2.authorize_security_group_ingress(
                GroupId=self.sg_id,
                IpPermissions=[
                    {
                        "FromPort": 80,
                        "ToPort": CONTAINER_APPLICATION_PORT,  # THIS MUST BE CHANGED TO THE CORRECT PORT NUMBER
                        "IpProtocol": "tcp",
                        "IpRanges": [
                            {
                                "CidrIp": "0.0.0.0/0",
                                "Description": "Allow HTTP traffic from anywhere"
                            }
                        ],
                        "Ipv6Ranges": [],
                        "PrefixListIds": [],
                        "UserIdGroupPairs": []
                    },
                    {
                        "FromPort": 433,
                        "ToPort": CONTAINER_APPLICATION_PORT,  # THIS MUST BE CHANGED TO THE CORRECT PORT NUMBER
                        "IpProtocol": "tcp",
                        "IpRanges": [
                            {
                                "CidrIp": "0.0.0.0/0",
                                "Description": "Allow HTTPS traffic from anywhere"
                            }
                        ],
                        "Ipv6Ranges": [],
                        "PrefixListIds": [],
                        "UserIdGroupPairs": []
                    }
                ]
            )
            Infrastructure.LOGGER.info("Security group ingress rules authorized successfully!")

    def _setup_role(self):
        try:
            self.iam.get_role(RoleName="AmazonEC2ContainerServiceforEC2Role")
            Infrastructure.LOGGER.warning("Instance profile role already exists! Skipping creation...")
        except self.iam.exceptions.NoSuchEntityException:
            Infrastructure.LOGGER.info("Creating Role...")
            role_policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {
                            "Service": "ec2.amazonaws.com"
                        },
                        "Action": "sts:AssumeRole"
                    }
                ]
            }

            self.iam.create_role(
                RoleName="AmazonEC2ContainerServiceforEC2Role",
                AssumeRolePolicyDocument=json.dumps(role_policy)
            )

            self.iam.attach_role_policy(
                RoleName="AmazonEC2ContainerServiceforEC2Role",
                PolicyArn="arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role"
            )

        try:
            self.instance_profile_arn = self.iam.get_instance_profile(
                InstanceProfileName=INSTANCE_PROFILE_NAME
            )["InstanceProfile"]["Arn"]
            Infrastructure.LOGGER.warning("Instance profile already exists! Skipping creation...")
        except Exception:
            Infrastructure.LOGGER.info("Creating instance profile...")
            instance_profile = self.iam.create_instance_profile(
                InstanceProfileName=INSTANCE_PROFILE_NAME
            )
            self.instance_profile_arn = instance_profile["InstanceProfile"]["Arn"]
            Infrastructure.LOGGER.info(
                f"Instance profile created successfully! Instance Profile ARN: {self.instance_profile_arn}")

            self.iam.add_role_to_instance_profile(
                InstanceProfileName=INSTANCE_PROFILE_NAME,
                RoleName="AmazonEC2ContainerServiceforEC2Role"
            )

            Infrastructure.LOGGER.info("Role added to instance profile successfully!")

    def _create_or_reuse_launch_template(self):
        lts = self.ec2.describe_launch_templates(
            Filters=[
                {
                    "Name": "launch-template-name",
                    "Values": [
                        ECS_LAUNCH_TEMPLATE_NAME
                    ]
                }
            ]
        )

        if len(lts["LaunchTemplates"]) > 0:
            Infrastructure.LOGGER.warning(f"Launch template with name {ECS_LAUNCH_TEMPLATE_NAME} already exists! "
                                          f"Reusing existing launch template...")
            self.ecs_launch_template_id = lts["LaunchTemplates"][0]["LaunchTemplateId"]
        else:
            # launch template is not found
            Infrastructure.LOGGER.info("Creating launch template...")

            launch_template = self.ec2.create_launch_template(
                LaunchTemplateName=ECS_LAUNCH_TEMPLATE_NAME,
                LaunchTemplateData={
                    "IamInstanceProfile": {
                        "Arn": self.instance_profile_arn
                    },
                    "BlockDeviceMappings": [
                        {
                            "DeviceName": "/dev/xvda",
                            "Ebs": {
                                "Encrypted": False,
                                "Iops": 3000,
                                "DeleteOnTermination": True,
                                "VolumeSize": 30,
                                "VolumeType": "gp3",
                                "Throughput": 300,
                            }
                        }
                    ],
                    "ImageId": ECS_IMAGE_AMI,  # CHANGE THIS TO YOUR AMI ID,
                    "InstanceType": "t2.micro",
                    "CreditSpecification": {
                        "CpuCredits": "standard"
                    },
                    "SecurityGroupIds": [
                        self.sg_id
                    ],
                    "UserData": base64.b64encode(
                        f"#!/bin/bash\necho ECS_CLUSTER={ECS_CLUSTER_NAME} >> /etc/ecs/ecs.config".encode()
                    ).decode('utf-8'),
                }
            )

            self.ecs_launch_template_id = launch_template["LaunchTemplate"]["LaunchTemplateId"]
            Infrastructure.LOGGER.info(
                f"Launch template created successfully! Launch Template ID: {self.ecs_launch_template_id}")

    def _create_or_reuse_auto_scaling_group(self):
        asgs = self.asg.describe_auto_scaling_groups(
            Filters=[
                {
                    "Name": "tag-key",
                    "Values": [
                        "Name"
                    ]
                },
                {
                    "Name": "tag-value",
                    "Values": [
                        ECS_ASG_NAME
                    ]
                }
            ]
        )

        if len(asgs["AutoScalingGroups"]) > 0:
            Infrastructure.LOGGER.warning(f"Auto scaling group with name {ECS_ASG_NAME} already exists! "
                                          f"Reusing existing auto scaling group...")
            self.asg_arn = asgs["AutoScalingGroups"][0]["AutoScalingGroupARN"]
        else:
            Infrastructure.LOGGER.info("Creating auto scaling group...")
            self.asg.create_auto_scaling_group(
                AutoScalingGroupName="ssg-wsg-asg",
                LaunchTemplate={
                    "LaunchTemplateId": self.ecs_launch_template_id,
                    "Version": "$Latest"
                },
                MaxSize=1,
                MinSize=1,
                DesiredCapacity=1,
                AvailabilityZones=["ap-southeast-1a", "ap-southeast-1b", "ap-southeast-1c"],
                VPCZoneIdentifier=f"{self.subnet_id_1},{self.subnet_id_2},{self.subnet_id_3}",
                Tags=[
                    {
                        "ResourceType": "auto-scaling-group",
                        "Key": "Name",
                        "Value": ECS_ASG_NAME,
                        "PropagateAtLaunch": True
                    }
                ]
            )

            group_details = self.asg.describe_auto_scaling_groups(
                Filters=[
                    {
                        "Name": "tag-key",
                        "Values": [
                            "Name"
                        ]
                    },
                    {
                        "Name": "tag-value",
                        "Values": [
                            ECS_ASG_NAME
                        ]
                    }
                ]
            )
            self.asg_arn = group_details["AutoScalingGroups"][0]["AutoScalingGroupARN"]
            Infrastructure.LOGGER.info(f"Auto scaling group created successfully! ASG ARN: {self.asg_arn}")

    def _create_or_reuse_ecr_repo(self):
        try:
            repos = self.ecr.describe_repositories(
                repositoryNames=[
                    os.getenv("ECR_REPO_NAME")
                ]
            )

            Infrastructure.LOGGER.warning(
                f"ECR repository with name {ECR_REPO_NAME} already exists! Reusing existing repository...")
        except ClientError:
            Infrastructure.LOGGER.info("Creating ECR repository...")
            registry = self.ecr.describe_registry()
            repo = self.ecr.create_repository(
                repositoryName=ECR_REPO_NAME,
                registryId=registry["registryId"]
            )
            Infrastructure.LOGGER.info(
                f"ECR repository created successfully! Repository URI: {repo['repository']['repositoryUri']}")

    def _create_or_reuse_capacity_provider(self):
        try:
            self.ecs.describe_capacity_providers(
                capacityProviders=[
                    ECS_CAPACITY_PROVIDER_NAME
                ]
            )

            Infrastructure.LOGGER.warning(f"Capacity provider with name {ECS_CAPACITY_PROVIDER_NAME} already exists! "
                                          f"Checking to ensure that it is active...")

            if any(map(lambda x: x["status"] != "ACTIVE", self.ecs.describe_capacity_providers(
                    capacityProviders=[
                        ECS_CAPACITY_PROVIDER_NAME
                    ])["capacityProviders"])):
                Infrastructure.LOGGER.warning("Capacity provider is inactive! Deleting capacity provider and "
                                              "attempting to re-create it...")
                self.ecs.delete_capacity_provider(
                    capacityProvider=ECS_CAPACITY_PROVIDER_NAME
                )
                Infrastructure.LOGGER.info("Capacity provider deleted!")

                self.ecs.create_capacity_provider(
                    name=ECS_CAPACITY_PROVIDER_NAME,
                    autoScalingGroupProvider={
                        "autoScalingGroupArn": self.asg_arn,
                    }
                )
                Infrastructure.LOGGER.info("Capacity provider recreated successfully!")
            else:
                Infrastructure.LOGGER.warning("Capacity provider is active! Reusing existing capacity provider...")
        except ClientError:
            # errors out as the capacity provider name does not exist and has failed to describe the capacity provider
            Infrastructure.LOGGER.info("Creating capacity provider...")
            self.ecs.create_capacity_provider(
                name=ECS_CAPACITY_PROVIDER_NAME,
                autoScalingGroupProvider={
                    "autoScalingGroupArn": self.asg_arn,
                }
            )

            Infrastructure.LOGGER.info("Capacity provider created successfully!")

    def _create_or_reuse_ecs_cluster(self):
        try:
            clusters = self.ecs.describe_clusters(
                clusters=[
                    ECS_CLUSTER_NAME
                ]
            )

            # reuse cluster
            Infrastructure.LOGGER.warning(
                f"ECS cluster with name {ECS_CLUSTER_NAME} already exists! Checking to ensure that it is active...")

            if any(map(lambda x: x["status"] != "ACTIVE", clusters["clusters"])):
                Infrastructure.LOGGER.warning("Cluster is inactive! Deleting cluster and attempting to re-create it...")
                self.ecs.delete_cluster(
                    cluster=ECS_CLUSTER_NAME
                )
                Infrastructure.LOGGER.info("Cluster deleted!")

                create_cluster = self.ecs.create_cluster(
                    clusterName=ECS_CLUSTER_NAME,
                    capacityProviders=[
                        ECS_CAPACITY_PROVIDER_NAME
                    ]
                )
                self.ecs_cluster_arn = create_cluster["cluster"]["clusterArn"]
                Infrastructure.LOGGER.info(f"Cluster recreated! Cluster ARN: {create_cluster['cluster']['clusterArn']}")
            else:
                active = list(filter(lambda x: x["status"] == "ACTIVE", clusters["clusters"]))[0]
                Infrastructure.LOGGER.warning("Cluster is active! Reusing existing cluster...")
                self.ecs_cluster_arn = active["clusterArn"]
        except ClientError:
            # cluster must be missing as it is failing to describe it
            Infrastructure.LOGGER.info("Creating ECS cluster...")
            create_cluster = self.ecs.create_cluster(
                clusterName=ECS_CLUSTER_NAME,
                capacityProviders=[
                    ECS_CAPACITY_PROVIDER_NAME
                ]
            )
            self.ecs_cluster_arn = create_cluster["cluster"]["clusterArn"]
            Infrastructure.LOGGER.info(
                f"ECS cluster created successfully! Cluster ARN: {create_cluster['cluster']['clusterArn']}")


if __name__ == '__main__':
    Infrastructure()
