module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = "${var.namespace}-${terraform.workspace}-vpc"
  cidr = var.vpc_cidr

  azs             = var.vpc_azs
  public_subnets  = var.vpc_public_subnets
  private_subnets = var.vpc_private_subnets

  enable_flow_log      = false
  enable_nat_gateway   = true
  single_nat_gateway   = true
  enable_vpn_gateway   = false
  enable_dns_hostnames = true

  public_subnet_tags = {
    Name = "${var.namespace}-${terraform.workspace}-public"
    Tier = "public"
  }

  private_subnet_tags = {
    Name = "${var.namespace}-${terraform.workspace}-private"
    Tier = "private"
  }
}

resource "aws_security_group" "vpc_endpoint_security_group" {
  name = "${var.namespace}-${terraform.workspace}-vpc-endpoint-sg"
  vpc_id = module.vpc.vpc_id

  ingress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = [var.vpc_cidr]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = [var.vpc_cidr]
  }
}
