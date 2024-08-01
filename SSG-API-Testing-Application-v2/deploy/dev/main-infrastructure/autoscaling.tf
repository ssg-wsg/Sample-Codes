# Target Tracking on ECS Cluster Task level
resource "aws_appautoscaling_target" "ecs_target" {
  max_capacity       = module.constants.max_task_count
  min_capacity       = module.constants.min_task_count
  resource_id        = "service/${aws_ecs_cluster.default.name}/${aws_ecs_service.default.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

# Target Tracking on ECS Cluster CPU Utilization
resource "aws_appautoscaling_policy" "ecs_cpu_policy" {
  name               = "${module.constants.namespace}-ecs-cpu-policy"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.ecs_target.resource_id
  scalable_dimension = aws_appautoscaling_target.ecs_target.scalable_dimension
  service_namespace  = aws_appautoscaling_target.ecs_target.service_namespace

  target_tracking_scaling_policy_configuration {
    target_value = module.constants.cpu_target_tracking_desired_value

    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }
  }
}

# Target Tracking on ECS Cluster Memory Utilization
resource "aws_appautoscaling_policy" "ecs_memory_policy" {
  name               = "${module.constants.namespace}-ecs-memory-policy"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.ecs_target.resource_id
  scalable_dimension = aws_appautoscaling_target.ecs_target.scalable_dimension
  service_namespace  = aws_appautoscaling_target.ecs_target.service_namespace

  target_tracking_scaling_policy_configuration {
    target_value = module.constants.memory_target_tracking_desired_value

    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageMemoryUtilization"
    }
  }
}

# Create ASG
resource "aws_autoscaling_group" "ecs_autoscaling_group" {
  name                  = "${module.constants.namespace}-asg"
  max_size              = module.constants.autoscaling_max_size
  min_size              = module.constants.autoscaling_min_size
  vpc_zone_identifier   = aws_subnet.private.*.id
  health_check_type     = "EC2"
  protect_from_scale_in = true # must be true as managed_termination_protection is enabled in capacity provider

  enabled_metrics = [
    "GroupMinSize",
    "GroupMaxSize",
    "GroupDesiredCapacity",
    "GroupInServiceInstances",
    "GroupPendingInstances",
    "GroupStandbyInstances",
    "GroupTerminatingInstances",
    "GroupTotalInstances"
  ]

  launch_template {
    id      = aws_launch_template.ecs_launch_template.id
    version = "$Latest"
  }

  instance_refresh {
    strategy = "Rolling"
  }

  lifecycle {
    create_before_destroy = true
  }

  tag {
    key                 = "Name"
    value               = "${module.constants.namespace}-asg"
    propagate_at_launch = true
  }
}