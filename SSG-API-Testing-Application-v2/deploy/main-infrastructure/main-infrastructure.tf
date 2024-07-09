# define ENV variables
variable "REPO_URL" {
  description = "The URL of the Docker repository to be created by ECR"
  type        = string
}

module "constants" {
  source = "../modules/constants"
}

# Specify dependencies
terraform {
  backend "s3" {
    bucket         = "ssg-tf-bucket"     # module.constants.TF_BUCKET_NAME
    key            = "main/main.tfstate" # module.constants.TF_MAIN_BUCKET_FILE_KEY
    region         = "ap-southeast-1"    # module.constants.AWS_REGION
    dynamodb_table = "ssg-tf-state-lock" # module.constants.TF_DYNAMODB_TABLE_NAME
    encrypt        = true
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws",
      version = "5.17.0"
    }
  }
}

provider "aws" {
  region = module.constants.AWS_REGION
}

# Create VPC
data "aws_availability_zones" "available" {
  state = "available"
}

locals {
  azs_count = 3
  azs_name  = data.aws_availability_zones.available.names
}

resource "aws_vpc" "main" {
  cidr_block           = module.constants.CIDR_BLOCK
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name = "ssg-vpc"
  }
}

resource "aws_subnet" "public" {
  count  = local.azs_count
  vpc_id = aws_vpc.main.id
  cidr_block = element([module.constants.SUBNET_CIDR_ONE,
    module.constants.SUBNET_CIDR_TWO,
  module.constants.SUBNET_CIDR_THREE], count.index)
  availability_zone       = element(local.azs_name, count.index)
  map_public_ip_on_launch = true
  tags = {
    Name = "ssg-public-subnet-${count.index + 1}"
  }
}

# Create IGW
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  tags = {
    Name = module.constants.INTERNET_GATEWAY_NAME
  }
}

# avoid creating Elastic IP for AZs, incurs cost
# resource "aws-eip" "main" {
#   count = local.azs_count
#   depends_on = [aws_internet_gateway.main]
#   tags = {
#     Name = "ssg-eip-${count.index + 1}"
#   }
# }

# Create Public Routing Tables
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  tags = {
    Name = module.constants.ROUTE_TABLE_NAME
  }
  route {
    cidr_block = module.constants.IPV4_ALL_CIDR
    gateway_id = aws_internet_gateway.main.id
  }
}

resource "aws_route_table_association" "public" {
  count          = local.azs_count
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

# Create ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = module.constants.ECS_CLUSTER_NAME
}

# Create ECS Role
data "aws_iam_policy_document" "ecs_node_doc" {
  statement {
    actions = ["sts:AssumeRole"]
    effect  = "Allow"

    principals {
      type        = "Service"
      identifiers = ["ecs.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "ecs_node_role" {
  name_prefix        = module.constants.IAM_ROLE_NAME
  assume_role_policy = data.aws_iam_policy_document.ecs_node_doc.json
}

resource "aws_iam_role_policy_attachment" "ecs_node_role_policy" {
  role       = aws_iam_role.ecs_node_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role"
}

resource "aws_iam_instance_profile" "ecs_node" {
  name_prefix = module.constants.IAM_INSTANCE_PROFILE
  path        = "/ecs/instance/"
  role        = aws_iam_role.ecs_node_role.name
}

# Create Security Group for ECS
resource "aws_security_group" "ecs_node_sg" {
  name_prefix = module.constants.SECURITY_GROUP_NAME
  vpc_id      = aws_vpc.main.id

  # SG permits egress from any port to any IP address
  egress {
    from_port        = 0
    to_port          = 65535
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
}

# Create Launch Template
data "aws_ssm_parameter" "ecs_node_ami" {
  name = "/aws/service/ecs/optimized-ami/amazon-linux-2/recommended/image_id"
}

resource "aws_launch_template" "ec2" {
  name_prefix            = module.constants.ECS_LAUNCH_TEMPLATE_NAME
  image_id               = data.aws_ssm_parameter.ecs_node_ami.value
  instance_type          = module.constants.ECS_LAUNCH_TEMPLATE_INSTANCE_TYPE
  vpc_security_group_ids = [aws_security_group.ecs_node_sg.id]

  iam_instance_profile {
    arn = aws_iam_instance_profile.ecs_node.arn
  }

  monitoring {
    enabled = false
  }

  user_data = base64encode(<<-EOF
    #!/bin/bash
    echo ECS_CLUSTER=${module.constants.ECS_CLUSTER_NAME} >> /etc/ecs/ecs.config;
    EOF
  )
}

# Create ASG
resource "aws_autoscaling_group" "ecs-asg" {
  name                      = module.constants.ECS_ASG_NAME
  vpc_zone_identifier       = aws_subnet.public[*].id
  min_size                  = module.constants.MIN_ASG_SIZE
  max_size                  = module.constants.MAX_ASG_SIZE
  health_check_grace_period = 0
  health_check_type         = "EC2"
  protect_from_scale_in     = false

  launch_template {
    id      = aws_launch_template.ec2.id
    version = "$Latest"
  }

  tag {
    key                 = "Name"
    value               = module.constants.ECS_CLUSTER_NAME
    propagate_at_launch = true
  }

  tag {
    key                 = "AmazonECSManaged"
    value               = ""
    propagate_at_launch = true
  }
}

# Create a Capacity Provider
resource "aws_ecs_capacity_provider" "main" {
  name = module.constants.ECS_CAPACITY_PROVIDER_NAME

  auto_scaling_group_provider {
    auto_scaling_group_arn         = aws_autoscaling_group.ecs-asg.arn
    managed_termination_protection = "DISABLED"

    managed_scaling {
      maximum_scaling_step_size = module.constants.MIN_ASG_SIZE
      minimum_scaling_step_size = module.constants.MIN_ASG_SIZE
      status                    = "ENABLED"
      target_capacity           = module.constants.MIN_ASG_SIZE
    }
  }
}

resource "aws_ecs_cluster_capacity_providers" "main" {
  cluster_name = aws_ecs_cluster.main.name
  capacity_providers = [
    aws_ecs_capacity_provider.main.name
  ]

  default_capacity_provider_strategy {
    capacity_provider = aws_ecs_capacity_provider.main.name
    base              = module.constants.MIN_ASG_SIZE
    weight            = 1
  }
}

# Create ECS Task Role
data "aws_iam_policy_document" "ecs_task_doc" {
  statement {
    actions = ["sts:AssumeRole"]
    effect  = "Allow"

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "ecs_task_role" {
  name_prefix        = "demo-ecs-task-role"
  assume_role_policy = data.aws_iam_policy_document.ecs_task_doc.json
}

resource "aws_iam_role" "ecs_exec_role" {
  name_prefix        = "demo-ecs-exec-role"
  assume_role_policy = data.aws_iam_policy_document.ecs_task_doc.json
}

resource "aws_iam_role_policy_attachment" "ecs_exec_role_policy" {
  role       = aws_iam_role.ecs_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_ecs_task_definition" "app" {
  family             = module.constants.ECS_TASK_DEFINITION_FAMILY
  task_role_arn      = aws_iam_role.ecs_task_role.arn
  execution_role_arn = aws_iam_role.ecs_exec_role.arn
  network_mode       = "awsvpc"
  cpu                = module.constants.ECS_TASK_CPU
  memory             = module.constants.ECS_TASK_MEMORY

  container_definitions = jsonencode([{
    name      = module.constants.ECS_CONTAINER_NAME,
    image     = "${var.REPO_URL}:latest",
    essential = true,
    portMappings = [
      {
        containerPort = module.constants.CONTAINER_APPLICATION_PORT,
        hostPort      = 80
      }
    ]
  }])
}


# Create ECS Service
resource "aws_ecs_service" "app" {
  name            = module.constants.ECS_SERVICE_NAME
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = module.constants.MIN_ASG_SIZE

  network_configuration {
    security_groups = [aws_security_group.ecs_task.id]
    subnets         = aws_subnet.public[*].id
  }

  capacity_provider_strategy {
    capacity_provider = aws_ecs_capacity_provider.main.name
    base              = module.constants.MIN_ASG_SIZE
    weight            = 100
  }

  ordered_placement_strategy {
    type  = "spread"
    field = "attribute:ecs.availability-zone"
  }

  lifecycle {
    ignore_changes = [desired_count]
  }

  depends_on = [aws_lb_target_group.app]

  load_balancer {
    target_group_arn = aws_lb_target_group.app.arn
    container_name   = module.constants.ECS_CONTAINER_NAME
    container_port   = 80
  }
}

# Create ECS Security Group
resource "aws_security_group" "ecs_task" {
  name_prefix = module.constants.ECS_SECURITY_GROUP_NAME
  description = "Allow all traffic within the VPC"
  vpc_id      = aws_vpc.main.id

  # Permit ingress from any port within the VPC
  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [aws_vpc.main.cidr_block]
  }

  # Permit egress from any port within the VPC
  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = [module.constants.IPV4_ALL_CIDR]
    ipv6_cidr_blocks = [module.constants.IPV6_ALL_CIDR]
  }
}

# Need an ALB to reach the ECS Service
resource "aws_security_group" "http_access" {
  name_prefix = module.constants.SECURITY_GROUP_NAME
  description = "Allow HTTP/S access"
  vpc_id      = aws_vpc.main.id

  dynamic "ingress" {
    for_each = [80, 443]
    content {
      protocol         = "tcp"
      from_port        = ingress.value
      to_port          = ingress.value
      cidr_blocks      = [module.constants.IPV4_ALL_CIDR]
      ipv6_cidr_blocks = [module.constants.IPV6_ALL_CIDR]
    }
  }

  egress {
    protocol         = "-1"
    from_port        = 0
    to_port          = 0
    cidr_blocks      = [module.constants.IPV4_ALL_CIDR]
    ipv6_cidr_blocks = [module.constants.IPV6_ALL_CIDR]
  }
}

resource "aws_lb" "main" {
  name               = module.constants.ALB_NAME
  load_balancer_type = "application"
  subnets            = aws_subnet.public[*].id
  security_groups    = [aws_security_group.http_access.id]
}

resource "aws_lb_target_group" "app" {
  name_prefix = module.constants.TARGET_GROUP_NAME
  vpc_id      = aws_vpc.main.id
  protocol    = "HTTP"
  port        = 80
  target_type = "ip"

  health_check {
    enabled             = true
    path                = "/"
    port                = 80
    matcher             = 200
    interval            = 10
    timeout             = 5
    healthy_threshold   = 8
    unhealthy_threshold = 2
  }
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.main.id
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app.id
  }
}

output "alb_url" {
  value = aws_lb.main.dns_name
}
