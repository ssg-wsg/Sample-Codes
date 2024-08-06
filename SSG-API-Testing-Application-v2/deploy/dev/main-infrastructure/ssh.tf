# Create Bastion Host
resource "aws_instance" "bastion_host" {
  ami                         = data.aws_ami.am2.id
  instance_type               = module.constants.bastion_host_instance_type
  subnet_id                   = aws_subnet.public[0].id
  associate_public_ip_address = true
  key_name                    = aws_key_pair.default.id
  vpc_security_group_ids      = [aws_security_group.bastion_host.id]

  tags = {
    Name = "${module.constants.namespace}-ec2-bastion-host"
  }
}
