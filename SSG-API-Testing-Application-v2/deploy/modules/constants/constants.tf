# pattern taken from https://stackoverflow.com/questions/59584420/how-to-define-global-variables-in-terraform
# create-backend constants
output "dynamodb_table_name" {
  value = "ssg-terraform-state-lock"
}

output "dynamodb_table_hash_key" {
  value = "LockID"
}

# ecr constants
output "ecr_s3_state_bucket_name" {
  value = "main/ecr.tfstate"
}

# main infrastructure constants
output "main_state_bucket_name" {
  value = "main/infrastructure.tfstate"
}

output "aws_region" {
  value = "ap-southeast-1"
}

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
  value = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDVLkiG61Z6tcziVlMDL3TWcFJbDGFJRv8e98lbGNZKMtOzTf++wIzJYuSvS+RK/sM/Gqql4nxagRhSKh6cx+KAYzd4zbMjrqvlRYXEWoQwD+/xm160A+R7ecGSEhbwxVigkJqAx9HGzMvO0o07oLtUz3NZxNEMLiIw8ZE0VjkCTa2gzaD3Rs3SFuPcsruc8wr0S+4ybazlx+Y1if7qWEGtixVtsBS3U89XK29amNr3HliPUPrvjcuh5Y4feI3f3mmGVvRCbmqkahfC2i6h9BKOI2c8Z4ZNRD/YAsMwe3GbZw8mk4rIztHHKIsubyjOGrqbWyO24/hKB2ooQVGE+9jM/YUD5dq8TyC9JniKgGVSlZSudfBTYsi/3fH76gO7i0vmNTL10Yf2zxYoVsWbeYvsId83RFbNZ3L6wlZngg6DFFAEtB5OUeMFKts+B/fq1ykJPD8DNyDfZtuI5C54oddxs+8oEDCGJWyl/1SkrHNGhKXcpPdLoKex3iVNw0whOBZS8t7Jru4/vy2CYNlRt3lnPjt+4Up+6H70F9jsJCxRTN5kFZQxJv+vWSAZwVqxNxx7IcY7N/bWTeajnoyXoglmERDhGToRsGPXf0V0gMsdzNcmKO6HuSyHYjw/U5ZOJQOil1vk4GDuDUspIxjlz4bmf78ppuDzxkjvwIxZu+VtaQ== george@Georges-MacBook-Pro.local"
}

output "az_count" {
  value = 1
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

output "deployment_maximum_percent" {
  value = 100
}

output "deployment_minimum_healthy_percent" {
  value = 50
}

output "launch_instance_instance_type" {
  value = "t2.micro"
}

output "broadcast_ipv4" {
  value = "0.0.0.0/0"
}
