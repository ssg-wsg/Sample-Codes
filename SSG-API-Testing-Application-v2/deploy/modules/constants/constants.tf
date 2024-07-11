# pattern taken from https://stackoverflow.com/questions/59584420/how-to-define-global-variables-in-terraform
output "AWS_REGION" {
  value = "ap-southeast-1"
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
  value = "tg-"
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
  value = 80
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

# NEW VARS
output "namespace" {
  value = "ssg"
}

output "service_name" {
  value = "sample-application"
}

output "cidr" {
  value = "172.16.0.0/16"
}

output "ssh_public_key" {
  value = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDCdenkTi5lBNuMjZH8awdfHQbabLqQ0toxiCkHoCBsCHoH7K+BHPg04P1YxGSJsmJz6Z+hsvk4EoxTUBfJpzsre6FqIk9OUcTFxHT7/VxVx33WCCedkJdTwlFpTFwo6hpHfuQx0fgWBWgk2gfNyfQ3Y5Xmo77gFwNxBauVEexQoiu7ArRIhkY/N9CjvUTQlX0FVK0r392wop8ux4ThqKJ3Whl0CYrNtHHDAwv84jmBE96EAD2klhg/qiyYmIEfW9Q+opv4ciyxFeP05Nu7KBlepSPa1fp7KPzBEQEjkywQSKQ+EvRWabgS/0Jv+oxHiI1GsdNV7gMo6iV+a8gcfyjh george@Georges-MacBook-Pro.local"
}

output "az_count" {
  value = 3
}

output "desired_instances_count" {
  value = 1
}

output "target_capacity" {
  value = 1
}

output "container_port" {
  value = 80
}

output "cpu" {
  value = 512
}

output "memory" {
  value = 512
}

output "region" {
  value = "ap-southeast-1"
}

output "log_retention_duration" {
  value = 7
}

output "max_scale_step" {
  value = 1
}

output "min_scale_step" {
  value = 1
}

output "max_task_count" {
  value = 1
}

output "min_task_count" {
  value = 1
}

output "cpu_target_tracking_desired_value" {
  value = 50
}

output "memory_target_tracking_desired_value" {
  value = 50
}

output "autoscaling_max_size" {
  value = 1
}

output "autoscaling_min_size" {
  value = 1
}
