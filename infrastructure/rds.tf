resource "random_password" "password" {
  length  = 16
  special = false
}

resource "aws_db_instance" "database" {
  identifier             = "${var.namespace}-${terraform.workspace}-db"
  engine                 = "postgres"
  engine_version         = "12.10"
  instance_class         = "db.t2.micro"
  db_name                = "realworld"
  username               = "realworld"
  password               = random_password.password.result
  vpc_security_group_ids = [aws_security_group.db_security_group.id]
  db_subnet_group_name   = aws_db_subnet_group.db_subnet_group.id
  skip_final_snapshot    = true
  allocated_storage      = 10
}

resource "aws_db_subnet_group" "db_subnet_group" {
  name       = "${var.namespace}-${terraform.workspace}-subnet-group"
  subnet_ids = module.vpc.private_subnets
}

resource "aws_security_group" "db_security_group" {
  name = "${var.namespace}-${terraform.workspace}-db-sg"
  vpc_id = module.vpc.vpc_id

  ingress {
    from_port = 5432
    protocol = "tcp"
    to_port = 5432
    cidr_blocks = [var.vpc_cidr]
  }

}
