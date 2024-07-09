# pattern taken from https://stackoverflow.com/questions/59584420/how-to-define-global-variables-in-terraform
output "AWS_REGION" {
  value = "ap-southeast-1"
}

output "CIDR_BLOCK" {
  value = "172.16.0.0/16"
}

output "SUBNET_CIDR_ONE" {
  value = "172.16.0.0/19"
}

output "SUBNET_CIDR_TWO" {
  value = "172.16.32.0/19"
}

output "SUBNET_CIDR_THREE" {
  value = "172.16.64.0/19"
}

output "INTERNET_GATEWAY_NAME" {
  value = "ssg-igw"
}

output "EIP_NAME" {
  value = "ssg-eip"
}

output "ROUTE_TABLE_NAME" {
  value = "ssg-public-route-table"
}

output "IPV4_ALL_CIDR" {
  value = "0.0.0.0/0"
}

output "IPV6_ALL_CIDR" {
  value = "::/0"
}

output "IAM_ROLE_NAME" {
  value = "ssg-ecs-role-"
}

output "IAM_INSTANCE_PROFILE" {
  value = "ssg-ecs-profile-"
}

output "SECURITY_GROUP_NAME" {
  value = "ssg-ecs-sg-"
}

output "ALB_NAME" {
  value = "ssg-alb"
}

output "TARGET_GROUP_NAME" {
  value = "ssg-tg-"
}

output "ECS_SECURITY_GROUP_NAME" {
  value = "ssg-ecs-task-sg-"
}

output "ECS_CLUSTER_NAME" {
  value = "ssg-ecs-cluster"
}

output "ECS_LAUNCH_TEMPLATE_NAME" {
  value = "ssg-ecs-launch-template-"
}

output "ECS_LAUNCH_TEMPLATE_INSTANCE_TYPE" {
  value = "t2.micro"
}

output "ECS_ASG_NAME" {
  value = "ssg-ecs-asg"
}

output "MIN_ASG_SIZE" {
  value = 1
}

output "MAX_ASG_SIZE" {
  value = 1
}

output "ECS_CAPACITY_PROVIDER_NAME" {
  value = "ssg-capacity-provider"
}

output "ECR_REPO_NAME" {
  value = "ssg-sample-application"
}

output "ECS_TASK_DEFINITION_FAMILY" {
  value = "ssg-wsg-app-"
}

output "ECS_SERVICE_NAME" {
  value = "ssg-ecs-service"
}

output "ECS_TASK_MEMORY" {
  value = 256
}

output "ECS_TASK_CPU" {
  value = 256
}

output "CONTAINER_APPLICATION_PORT" {
  value = 8502
}

output "ECS_CONTAINER_NAME" {
  value = "app"
}

output "TF_BUCKET_NAME" {
  value = "ssg-tf-bucket"
}

output "TF_DYNAMODB_TABLE_NAME" {
  value = "ssg-tf-state-lock"
}

output "TF_ECR_BUCKET_FILE_KEY" {
  value = "ecr/ecr.tfstate"
}

output "TF_MAIN_BUCKET_FILE_KEY" {
  value = "main/main.tfstate"
}
