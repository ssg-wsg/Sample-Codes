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

output "ssl_cert" {
  value = <<EOF
  -----BEGIN CERTIFICATE-----"
  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
  -----END CERTIFICATE-----
EOF
}
