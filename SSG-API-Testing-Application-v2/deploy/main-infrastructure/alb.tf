# Create ALB in public subnet to forward traffic to ECS service
resource "aws_alb" "alb" {
  name = "${module.constants.namespace}-alb"
  security_groups = [aws_security_group.alb.id]
  subnets = aws_subnet.public.*.id
}

# Create HTTP listener
resource "aws_alb_listener" "alb_default_listener_https" {
  load_balancer_arn = aws_alb.alb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_alb_target_group.service_target_group.arn
  }
}

# Create TG
resource "aws_alb_target_group" "service_target_group" {
  name = "${module.constants.namespace}-targetGroup"
  port = "80"
  protocol = "HTTP"
  vpc_id = aws_vpc.default.id
  deregistration_delay = 120

  health_check {
    healthy_threshold = 2
    unhealthy_threshold = 2
    interval = 60
    matcher = "200-399"
    path = "/"
    port = "traffic-port"
    protocol = "HTTP"
    timeout = 30
  }

  depends_on = [aws_alb.alb]
}