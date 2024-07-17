# Create ECS cluster
resource "aws_ecs_cluster" "default" {
  name = "${module.constants.namespace}-ecs-cluster"

  lifecycle {
    create_before_destroy = true
  }

  tags = {
    Name = "${module.constants.namespace}-ecs-cluster"
  }
}

# Create ECS service
resource "aws_ecs_service" "default" {
  name                               = "${module.constants.namespace}-ecs-service"
  iam_role                           = aws_iam_role.ecs_service_role.arn
  cluster                            = aws_ecs_cluster.default.id
  task_definition                    = aws_ecs_task_definition.default.arn
  desired_count                      = module.constants.desired_instances_count
  deployment_maximum_percent         = module.constants.deployment_maximum_percent
  deployment_minimum_healthy_percent = module.constants.deployment_minimum_healthy_percent

  load_balancer {
    target_group_arn = aws_alb_target_group.service_target_group.arn
    container_name   = module.constants.service_name
    container_port   = module.constants.container_port
  }

  ordered_placement_strategy {
    type  = "spread"
    field = "attribute:ecs.availability-zone"
  }

  ordered_placement_strategy {
    type  = "binpack"
    field = "memory"
  }

  # We have to ignore desired_count changes as it may bypass capacity planning made by our autoscaling resources
  lifecycle {
    ignore_changes = [desired_count]
  }
}

# Create ECS Task Definition
resource "aws_ecs_task_definition" "default" {
  family             = "${module.constants.namespace}-ecs-task-definition"
  execution_role_arn = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn      = aws_iam_role.ecs_task_iam_role.arn
  depends_on         = [null_resource.image]

  container_definitions = jsonencode([
    {
      name      = module.constants.service_name
      image     = "${data.aws_ecr_repository.ecr.repository_url}:${local.hash}"
      cpu       = module.constants.cpu
      memory    = module.constants.memory
      essential = true
      portMappings = [
        {
          containerPort = module.constants.container_port
          hostPort      = 0
          protocol      = "tcp"
        }
      ]

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.cloudwatch_log_group.name
          "awslogs-region"        = module.constants.region
          "awslogs-stream-prefix" = module.constants.namespace
        }
      }
    }
  ])
}