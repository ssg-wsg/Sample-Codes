import os

from prettytable import PrettyTable

AWS_REGION = "ap-southeast-1"
CIDR_BLOCK = "172.16.0.0/16"
SUBNET_CIDR_ONE = "172.16.0.0/19"
SUBNET_CIDR_TWO = "172.16.32.0/19"
SUBNET_CIDR_THREE = "172.16.64.0/19"
INSTANCE_PROFILE_NAME = "ssg-ecs-instance-profile"
ECS_CLUSTER_NAME = "ssg-ecs-app"
ECS_IMAGE_AMI = "ami-0153fd8c2692db1b7"  # this is an AWS Linux 2023 ECS AMI
ECS_LAUNCH_TEMPLATE_NAME = "ssg-ecs-launch-template"
ECS_ASG_NAME = "ssg-ecs-asg"
ECS_CAPACITY_PROVIDER_NAME = "ssg-capacity-provider"
ECR_REPO_NAME = "ssg-sample-application"
SG_GROUP_NAME = "ssg-wsg-sg"
ECS_TASK_DEFINITION_FAMILY = "ssg-wsg-app"
ECS_SERVICE_NAME = "ssg-wsg-ecs-service"
ECS_TASK_MEMORY = 512
ECS_TASK_CPU = 512
CONTAINER_APPLICATION_PORT = 8502
ECS_CONTAINER_NAME = "app"  # should be the same as that defined in ecs.py 


def load():
    """Load environment variables into local environment or GitHub Environment file."""

    env_file = os.getenv("GITHUB_ENV")

    if env_file is None:
        os.putenv("AWS_REGION", AWS_REGION)
        os.putenv("CIDR_BLOCK", CIDR_BLOCK)
        os.putenv("SUBNET_CIDR_ONE", SUBNET_CIDR_ONE)
        os.putenv("SUBNET_CIDR_TWO", SUBNET_CIDR_TWO)
        os.putenv("SUBNET_CIDR_THREE", SUBNET_CIDR_THREE)
        os.putenv("INSTANCE_PROFILE_NAME", INSTANCE_PROFILE_NAME)
        os.putenv("ECS_CLUSTER_NAME", ECS_CLUSTER_NAME)
        os.putenv("ECS_IMAGE_AMI", ECS_IMAGE_AMI)
        os.putenv("ECS_LAUNCH_TEMPLATE_NAME", ECS_LAUNCH_TEMPLATE_NAME)
        os.putenv("ECS_ASG_NAME", ECS_ASG_NAME)
        os.putenv("ECS_CAPACITY_PROVIDER_NAME", ECS_CAPACITY_PROVIDER_NAME)
        os.putenv("ECR_REPO_NAME", ECR_REPO_NAME)
        os.putenv("SG_GROUP_NAME", SG_GROUP_NAME)
        os.putenv("ECS_TASK_DEFINITION_FAMILY", ECS_TASK_DEFINITION_FAMILY)
        os.putenv("ECS_SERVICE_NAME", ECS_SERVICE_NAME)
        os.putenv("ECS_TASK_MEMORY", str(ECS_TASK_MEMORY))
        os.putenv("ECS_TASK_CPU", str(ECS_TASK_CPU))
        os.putenv("CONTAINER_APPLICATION_PORT", str(CONTAINER_APPLICATION_PORT))
        os.putenv("ECS_CONTAINER_NAME", ECS_CONTAINER_NAME)

    with open(env_file, "a") as f:
        f.write(f"AWS_REGION={AWS_REGION}\n")
        f.write(f"CIDR_BLOCK={CIDR_BLOCK}\n")
        f.write(f"SUBNET_CIDR_ONE={SUBNET_CIDR_ONE}\n")
        f.write(f"SUBNET_CIDR_TWO={SUBNET_CIDR_TWO}\n")
        f.write(f"SUBNET_CIDR_THREE={SUBNET_CIDR_THREE}\n")
        f.write(f"INSTANCE_PROFILE_NAME={INSTANCE_PROFILE_NAME}\n")
        f.write(f"ECS_CLUSTER_NAME={ECS_CLUSTER_NAME}\n")
        f.write(f"ECS_IMAGE_AMI={ECS_IMAGE_AMI}")
        f.write(f"ECS_LAUNCH_TEMPLATE_NAME={ECS_LAUNCH_TEMPLATE_NAME}\n")
        f.write(f"ECS_ASG_NAME={ECS_ASG_NAME}\n")
        f.write(f"ECS_CAPACITY_PROVIDER_NAME={ECS_CAPACITY_PROVIDER_NAME}\n")
        f.write(f"ECR_REPO_NAME={ECR_REPO_NAME}\n")
        f.write(f"SG_GROUP_NAME={SG_GROUP_NAME}\n")
        f.write(f"ECS_TASK_DEFINITION_FAMILY={ECS_TASK_DEFINITION_FAMILY}\n")
        f.write(f"ECS_SERVICE_NAME={ECS_SERVICE_NAME}\n")
        f.write(f"ECS_TASK_MEMORY={ECS_TASK_MEMORY}\n")
        f.write(f"ECS_TASK_CPU={ECS_TASK_CPU}\n")
        f.write(f"CONTAINER_APPLICATION_PORT={CONTAINER_APPLICATION_PORT}\n")
        f.write(f"ECS_CONTAINER_NAME={ECS_CONTAINER_NAME}\n")


def echo_vars():
    """Print environment variables to console for reference."""

    ptable = PrettyTable(field_names=["Env. Variable", "Value"])
    ptable.add_row(["AWS_REGION", AWS_REGION])
    ptable.add_row(["CIDR_BLOCK", CIDR_BLOCK])
    ptable.add_row(["SUBNET_CIDR_ONE", SUBNET_CIDR_ONE])
    ptable.add_row(["SUBNET_CIDR_TWO", SUBNET_CIDR_TWO])
    ptable.add_row(["SUBNET_CIDR_THREE", SUBNET_CIDR_THREE])
    ptable.add_row(["INSTANCE_PROFILE_NAME", INSTANCE_PROFILE_NAME])
    ptable.add_row(["ECS_CLUSTER_NAME", ECS_CLUSTER_NAME])
    ptable.add_row(["ECS_IMAGE_AMI", ECS_IMAGE_AMI])
    ptable.add_row(["ECS_LAUNCH_TEMPLATE_NAME", ECS_LAUNCH_TEMPLATE_NAME])
    ptable.add_row(["ECS_ASG_NAME", ECS_ASG_NAME])
    ptable.add_row(["ECS_CAPACITY_PROVIDER_NAME", ECS_CAPACITY_PROVIDER_NAME])
    ptable.add_row(["ECR_REPO_NAME", ECR_REPO_NAME])
    ptable.add_row(["SG_GROUP_NAME", SG_GROUP_NAME])
    ptable.add_row(["ECS_TASK_DEFINITION_FAMILY", ECS_TASK_DEFINITION_FAMILY])
    ptable.add_row(["ECS_SERVICE_NAME", ECS_SERVICE_NAME])
    ptable.add_row(["ECS_TASK_MEMORY", ECS_TASK_MEMORY])
    ptable.add_row(["ECS_TASK_CPU", ECS_TASK_CPU])
    ptable.add_row(["CONTAINER_APPLICATION_PORT", CONTAINER_APPLICATION_PORT])
    ptable.add_row(["ECS_CONTAINER_NAME", ECS_CONTAINER_NAME])

    print(ptable)


if __name__ == '__main__':
    load()
    echo_vars()
