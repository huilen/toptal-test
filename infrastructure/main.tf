terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

terraform {
  backend "s3" {
    bucket = "realworld-terraform-state"
    key = "terraform.tfstate"
    region = "us-east-1"
  }
}

data "aws_caller_identity" "current" {}
