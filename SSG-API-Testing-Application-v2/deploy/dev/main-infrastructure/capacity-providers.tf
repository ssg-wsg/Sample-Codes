resource "aws_ecs_capacity_provider" "cas" {
  name = "${module.constants.namespace}-${module.constants.service_name}-capacity-provider"

  auto_scaling_group_provider {
    auto_scaling_group_arn         = aws_autoscaling_group.ecs_autoscaling_group.arn
    managed_termination_protection = "ENABLED"

    managed_scaling {
      maximum_scaling_step_size = module.constants.max_scale_step
      minimum_scaling_step_size = module.constants.min_scale_step
      status                    = "ENABLED"
      target_capacity           = module.constants.target_capacity
    }
  }
}

resource "aws_ecs_cluster_capacity_providers" "cas" {
  cluster_name       = aws_ecs_cluster.default.name
  capacity_providers = [aws_ecs_capacity_provider.cas.name]
}
