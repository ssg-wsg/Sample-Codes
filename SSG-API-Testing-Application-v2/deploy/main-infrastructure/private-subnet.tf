# Create private subnet with NAT gateway
# NAT gateway required for public internet access
# Create EIP for each AZ
resource "aws_eip" "nat_gateway" {
  count  = module.constants.az_count
  domain = "vpc"

  tags = {
    Name = "${module.constants.namespace}_eip_${count.index}"
  }
}

# Create one NAT per AZ
resource "aws_nat_gateway" "nat_gateway" {
  count         = module.constants.az_count
  subnet_id     = aws_subnet.public[count.index].id
  allocation_id = aws_eip.nat_gateway[count.index].id

  tags = {
    Name = "${module.constants.namespace}_privateSubnet_${count.index}"
  }
}

# Create private subnets
resource "aws_subnet" "private" {
  count             = module.constants.az_count
  cidr_block        = cidrsubnet(module.constants.cidr, 8, count.index)
  availability_zone = data.aws_availability_zones.available.names[count.index]
  vpc_id            = aws_vpc.default.id

  tags = {
    Name = "${module.constants.namespace}_privateSubnet_${count.index}"
  }
}

# Create private routing table
resource "aws_route_table" "private" {
  count  = module.constants.az_count
  vpc_id = aws_vpc.default.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat_gateway[count.index].id
  }

  tags = {
    Name = "${module.constants.namespace}_privateRouteTable_${count.index}"
  }
}

# Create private route table association
resource "aws_route_table_association" "private" {
  count          = module.constants.az_count
  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private[count.index].id
}
