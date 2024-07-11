# Create EC2 Security Group
resource "aws_security_group" "ec2" {
  name        = "${module.constants.namespace}_ec2_sg"
  description = "Security group for EC2 instances"
  vpc_id      = aws_vpc.default.id

  ingress {
    from_port       = 1024
    to_port         = 65535
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  ingress {
    from_port       = 22
    to_port         = 22
    protocol        = "tcp"
    security_groups = [aws_security_group.bastion_host.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${module.constants.namespace}_ec2_sg"
  }
}

# Create ALB SG
resource "aws_security_group" "alb" {
  name        = "${module.constants.namespace}_alb_sg"
  description = "Security group for ALB"
  vpc_id      = aws_vpc.default.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${module.constants.namespace}_alb_sg"
  }
}

# Create Bastion Host SG
resource "aws_security_group" "bastion_host" {
  name        = "${module.constants.namespace}_bastion_host_sg"
  description = "Security group for Bastion Host"
  vpc_id      = aws_vpc.default.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}