# pattern taken from https://stackoverflow.com/questions/59584420/how-to-define-global-variables-in-terraform
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
