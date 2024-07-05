"""
IaC template for creating base cloud environment

Inspired from https://aws.plainenglish.io/creating-vpc-using-boto3-terraform-cloudformation-and-both-af741a8afb3c
"""

import os

import boto3
import logging

from botocore.config import Config
from botocore.exceptions import ClientError

# define parameters to be used in the stack
LOGGER = logging.getLogger("infra")
LOGGER.setLevel(logging.INFO)
STREAM_HANDLER = logging.StreamHandler()
STREAM_HANDLER.setLevel(logging.INFO)
LOGGER.addHandler(STREAM_HANDLER)

config = Config(
    region_name="ap-southeast-1"  # CHANGE THIS TO YOUR REGION OF CHOICE
)

# set up VPC
ec2 = boto3.client("ec2", config=config)

LOGGER.info("Creating VPC...")
vpc = ec2.create_vpc(
    CidrBlock="172.16.0.0/16"
)
LOGGER.info(f"VPC created successfully! VPC ID: {vpc["Vpc"]["VpcId"]}")


# enable public DNS hostname for SSH
LOGGER.info("Enabling public DNS hostname for VPC...")
ec2.modify_vpc_attribute(
    VpcId=vpc["Vpc"]["VpcId"], EnableDnsSupport={"Value": True}
)
ec2.modify_vpc_attribute(
    VpcId=vpc["Vpc"]["VpcId"], EnableDnsHostnames={"Value": True}
)
LOGGER.info("Public DNS hostname for VPC enabled successfully!")

# create internet gateway
LOGGER.info("Creating internet gateway...")
ig = ec2.create_internet_gateway()
LOGGER.info(f"Internet gateway created successfully! Internet Gateway ID: {ig['InternetGateway']['InternetGatewayId']}")

LOGGER.info("Attaching IGW to VPC...")
ec2.attach_internet_gateway(
    VpcId=vpc["Vpc"]["VpcId"],
    InternetGatewayId=ig["InternetGateway"]["InternetGatewayId"]
)
LOGGER.info("IGW attached to VPC successfully!")


# create a routing table
LOGGER.info("Creating routing table...")
rt = ec2.create_route_table(VpcId=vpc["Vpc"]["VpcId"])
LOGGER.info(f"Routing table created successfully! Route Table ID: {rt['RouteTable']['RouteTableId']}")

# create a route to the internet gateway
LOGGER.info("Creating route to internet gateway...")
route = ec2.create_route(
    DestinationCidrBlock="0.0.0.0/0",
    GatewayId=ig["InternetGateway"]["InternetGatewayId"],
    RouteTableId=rt["RouteTable"]["RouteTableId"]
)
LOGGER.info("Route to internet gateway created successfully!")

# create subnets and associate it with the routing table
LOGGER.info("Creating subnets and associating them with the routing table...")
subnet1 = ec2.create_subnet(
    AvailabilityZone="ap-southeast-1a",
    CidrBlock="172.16.32.0/20",
    VpcId=vpc["Vpc"]["VpcId"]
)
LOGGER.info(f"Subnet 1 created successfully! Subnet ID: {subnet1['Subnet']['SubnetId']}")

subnet2 = ec2.create_subnet(
    AvailabilityZone="ap-southeast-1b",
    CidrBlock="172.16.16.0/20",
    VpcId=vpc["Vpc"]["VpcId"]
)
LOGGER.info(f"Subnet 2 created successfully! Subnet ID: {subnet2['Subnet']['SubnetId']}")

# associate the routing table with the subnets
table = boto3.resource("ec2").RouteTable(rt["RouteTable"]["RouteTableId"])

LOGGER.info("Associating routing table with subnets...")
table.associate_with_subnet(SubnetId=subnet1["Subnet"]["SubnetId"])
table.associate_with_subnet(SubnetId=subnet2["Subnet"]["SubnetId"])
LOGGER.info("Routing table associated with subnets successfully!")

# form the required Security Groups, Ingress Rules and Launch Templates
LOGGER.info("Creating security group...")
sg = ec2.create_security_group(
    Description="Security group for SSG-WSG Sample Application",
    GroupName=os.getenv("SG_GROUP_NAME"),
    VpcId=vpc["Vpc"]["VpcId"]  # CHANGE THIS TO YOUR VPC ID IN THE REGION
)
LOGGER.info(f"Security group created successfully! Security Group ID: {sg['GroupId']}")

LOGGER.info("Authorizing security group ingress rules...")
sg_ingress = ec2.authorize_security_group_ingress(
    GroupId=sg["GroupId"],
    IpPermissions=[
        {
            "FromPort": 80,
            "ToPort": 8502,  # THIS MUST BE CHANGED TO THE PORT NUMBER THAT THE APPLICATED IS SERVED ON
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
            "ToPort": 8502,  # THIS MUST BE CHANGED TO THE PORT NUMBER THAT THE APPLICATED IS SERVED ON
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
LOGGER.info("Security group ingress rules authorized successfully!")

# create launch template
LOGGER.info("Creating launch template...")
try:
    launch_template = ec2.create_launch_template(
        LaunchTemplateName="ssg-wsg-app-launch-template",
        LaunchTemplateData={
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
            "ImageId": "ami-0153fd8c2692db1b7",  # CHANGE THIS TO YOUR AMI ID,
            "InstanceType": "t2.micro",
            "CreditSpecification": {
                "CpuCredits": "standard"
            },
            "SecurityGroupIds": [
                sg["GroupId"]
            ]
        }
    )
    LOGGER.info(f"Launch template created successfully! "
                f"Launch Template ID: {launch_template['LaunchTemplate']['LaunchTemplateId']}")
except ClientError as ex:
    logging.error(f"Error creating launch template: {ex}")
    raise ex

# create ASG client
asg = boto3.client("autoscaling", config=config)

# create launch template
LOGGER.info("Creating auto scaling group...")
asg_group = asg.create_auto_scaling_group(
    AutoScalingGroupName="ssg-wsg-asg",
    LaunchTemplate={
        "LaunchTemplateId": launch_template["LaunchTemplate"]["LaunchTemplateId"],
        "Version": "$Latest"
    },
    MaxSize=1,
    MinSize=1,
    DesiredCapacity=1,
    AvailabilityZones=[
        "ap-southeast-1a",
        "ap-southeast-1b"
    ],
    VPCZoneIdentifier=f"{subnet1['Subnet']['SubnetId']},{subnet2['Subnet']['SubnetId']}",
)

group_details = asg.describe_auto_scaling_groups(
    AutoScalingGroupNames=["ssg-wsg-asg"]
)

LOGGER.info(f"Auto scaling group created successfully! "
            f"ASG ARN: {group_details['AutoScalingGroups'][0]['AutoScalingGroupARN']}")

# create ecr repo
ecr = boto3.client("ecr", config=config)

LOGGER.info("Creating ECR repository...")
registry = ecr.describe_registry()
repo = ecr.create_repository(
    repositoryName=os.getenv("ECR_REPO_NAME"),
    registryId=registry["registryId"]
)
LOGGER.info(f"ECR repository created successfully! Repository URI: {repo['repository']['repositoryUri']}")

# create ECS client
ecs = boto3.client("ecs", config=config)

# create capacity provider
LOGGER.info("Creating capacity provider...")
try:
    capacity_provider = ecs.create_capacity_provider(
        name="ssg-capacity-provider",
        autoScalingGroupProvider={
            "autoScalingGroupArn": group_details['AutoScalingGroups'][0]['AutoScalingGroupARN'],
        }
    )
    LOGGER.info(f"Capacity provider created successfully! Capacity Provider ARN: {capacity_provider['capacityProvider']['capacityProviderArn']}")
except ClientError as ex:
    LOGGER.info(f"Error: {ex}, attempting to delete and re-create the provider...")
    ecs.delete_capacity_provider(
        capacityProvider="ssg-capacity-provider"
    )
    capacity_provider = ecs.create_capacity_provider(
        name="ssg-capacity-provider",
        autoScalingGroupProvider={
            "autoScalingGroupArn": group_details['AutoScalingGroups'][0]['AutoScalingGroupARN'],
        }
    )
    LOGGER.info(
        f"Capacity provider created successfully! Capacity Provider ARN: {capacity_provider['capacityProvider']['capacityProviderArn']}")


# create ECS cluster
LOGGER.info("Creating ECS cluster...")
create_cluster = ecs.create_cluster(
    clusterName="ssg-ecs-app",
    capacityProviders=[
        "ssg-capacity-provider"
    ]
)
LOGGER.info(f"ECS cluster created successfully! Cluster ARN: {create_cluster['cluster']['clusterArn']}")

LOGGER.info(f"""
\n
############################################
!Infrastructure Setup Info!

Paste the following values into the 
integration.yml GitHub Actions file for
automated deployment!

--------------------------------------------

SUBNET1_ID: {subnet1["Subnet"]["SubnetId"]}
SUBNET2_ID: {subnet2["Subnet"]["SubnetId"]}
SECURITY_GROUP_ID: {sg['GroupId']}
ECS_CLUSTER_ARN: {create_cluster["cluster"]["clusterArn"]}

############################################
\n
""")

LOGGER.info("Writing environment variables to GitHub Actions environment file...")
github = os.getenv("GITHUB_ENV")
# taken from
# https://stackoverflow.com/questions/70123328/how-to-set-environment-variables-in-github-actions-using-python
env_file = os.getenv("GITHUB_ENV")

with open(env_file, "a") as f:
    f.write(f"SUBNET1_ID={subnet1["Subnet"]["SubnetId"]}\n")
    f.write(f"SUBNET2_ID={subnet2["Subnet"]["SubnetId"]}\n")
    f.write(f"SECURITY_GROUP_ID={sg['GroupId']}\n")
    f.write(f"ECS_CLUSTER_ARN={create_cluster['cluster']['clusterArn']}\n")

LOGGER.info("Environment variables written to GitHub Actions environment file successfully!")
LOGGER.info("Exiting...")
