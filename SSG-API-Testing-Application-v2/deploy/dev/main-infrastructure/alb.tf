# Create ALB in public subnet to forward traffic to ECS service
resource "aws_alb" "alb" {
  name            = "${module.constants.namespace}-alb"
  security_groups = [aws_security_group.alb.id]
  subnets         = aws_subnet.public.*.id
}

# Create HTTP listener
resource "aws_alb_listener" "alb_default_listener_http" {
  load_balancer_arn = aws_alb.alb.arn
  port              = 80 # HTTP Port
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_alb_target_group.service_target_group.arn
  }

  depends_on = [aws_alb.alb]
}

# Create TG
resource "aws_alb_target_group" "service_target_group" {
  name                 = "${module.constants.namespace}-target-group"
  port                 = "80"
  protocol             = "HTTP"
  vpc_id               = aws_vpc.default.id
  deregistration_delay = 300

  health_check {
    healthy_threshold   = 2
    unhealthy_threshold = 2
    interval            = 60
    matcher             = "200"
    path                = "/"
    port                = "traffic-port"
    protocol            = "HTTP"
    timeout             = 10
  }

  # stickiness to maintain session state
  stickiness {
    cookie_duration = 86400
    cookie_name     = "SSGWSGSAMPLEAPPCOOKIE"
    enabled         = true
    type            = "app_cookie"
  }

  depends_on = [aws_alb.alb]
}