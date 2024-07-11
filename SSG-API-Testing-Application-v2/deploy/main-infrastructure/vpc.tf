# Create VPC first
resource "aws_vpc" "default" {
  cidr_block           = module.constants.cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "${module.constants.namespace}_VPC_${module.constants.service_name}"
  }
}

# Create IGW next
resource "aws_internet_gateway" "default" {
  vpc_id = aws_vpc.default.id

  tags = {
    Name = "${module.constants.namespace}_IGW_${module.constants.service_name}"
  }
}

# Specify all available AZs
data "aws_availability_zones" "available" {}
