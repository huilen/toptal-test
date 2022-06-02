variable region {
  default = "us-east-1"
}

variable namespace {
  default = "realworld"
}

variable vpc_cidr {}

variable vpc_private_subnets {}

variable vpc_public_subnets {}

variable vpc_azs {}

variable "config" {
  type = map(string)
  default = {}
}

variable "secret" {
  default = null
}

variable "webapp_port" {
  default = 8000
}
variable "webapp_instances" {}
variable "webapp_debug" {}

variable "django_allowed_hosts" {}
variable "django_secret_key" {}
