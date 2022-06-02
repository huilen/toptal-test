resource "aws_ecr_repository" "ecr_nginx_repository" {
  name = "${var.namespace}-${terraform.workspace}-nginx"

  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_repository" "ecr_webapp_repository" {
  name = "${var.namespace}-${terraform.workspace}-webapp"

  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}
