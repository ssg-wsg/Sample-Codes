# Create Cloudwatch Log Group for application logging
resource "aws_cloudwatch_log_group" "cloudwatch_log_group" {
  name              = "${module.constants.namespace}/ecs/${module.constants.service_name}"
  retention_in_days = module.constants.log_retention_duration
}
