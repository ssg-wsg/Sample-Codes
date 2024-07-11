# Create public subnet and assoicated routing tables
resource "aws_subnet" "public" {
  count                   = module.constants.az_count
  cidr_block              = cidrsubnet(module.constants.cidr, 8, module.constants.az_count + count.index)
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  vpc_id                  = aws_vpc.default.id
  map_public_ip_on_launch = true

  tags = {
    Name = "${module.constants.namespace}_publicSubnet_${count.index}"
  }
}

# Create route table
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.default.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.default.id
  }

  tags = {
    Name = "${module.constants.namespace}_publicRouteTable"
  }
}

# Create public route table association
resource "aws_route_table_association" "public" {
  count          = module.constants.az_count
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

# Set our route table as the main route table
resource "aws_main_route_table_association" "public_main" {
  vpc_id         = aws_vpc.default.id
  route_table_id = aws_route_table.public.id
}
