# Create public subnet and assoicated routing tables
resource "aws_subnet" "public" {
  count                   = module.constants.az_count
  cidr_block              = cidrsubnet(module.constants.cidr, 8, module.constants.az_count + count.index)
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  vpc_id                  = aws_vpc.default.id
  map_public_ip_on_launch = true

  tags = {
    Name = "${module.constants.namespace}-public-subnet-${count.index}"
  }
}

# Create route table
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.default.id

  route {
    cidr_block = module.constants.broadcast_ipv4
    gateway_id = aws_internet_gateway.default.id
  }

  tags = {
    Name = "${module.constants.namespace}-public-route-table"
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

# NAT gateway required for public internet access
# Create EIP for each AZ
resource "aws_eip" "nat_gateway" {
  count  = module.constants.az_count
  domain = "vpc"

  tags = {
    Name = "${module.constants.namespace}-elastic-ip-${count.index}"
  }
}

# Create one NAT per AZ
resource "aws_nat_gateway" "nat_gateway" {
  count         = module.constants.az_count
  subnet_id     = aws_subnet.public[count.index].id
  allocation_id = aws_eip.nat_gateway[count.index].id

  tags = {
    Name = "${module.constants.namespace}-nat-gateway-${count.index}"
  }
}
