# Create private subnet with NAT gateway
resource "aws_subnet" "private" {
  count             = module.constants.az_count
  cidr_block        = cidrsubnet(module.constants.cidr, 8, count.index)
  availability_zone = data.aws_availability_zones.available.names[count.index]
  vpc_id            = aws_vpc.default.id

  tags = {
    Name = "${module.constants.namespace}-private-subnet-${count.index}"
  }
}

# Create private routing table
resource "aws_route_table" "private" {
  count  = module.constants.az_count
  vpc_id = aws_vpc.default.id

  route {
    cidr_block     = module.constants.broadcast_ipv4
    nat_gateway_id = aws_nat_gateway.nat_gateway[count.index].id
  }

  tags = {
    Name = "${module.constants.namespace}-private-route-table-${count.index}"
  }
}

# Create private route table association
resource "aws_route_table_association" "private" {
  count          = module.constants.az_count
  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private[count.index].id
}
