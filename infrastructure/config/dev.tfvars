vpc_cidr = "10.10.0.0/16"

vpc_private_subnets = [
  "10.10.10.0/24",
  "10.10.11.0/24",
  "10.10.12.0/24"
]

vpc_public_subnets = [
  "10.10.0.0/24",
  "10.10.1.0/24",
  "10.10.2.0/24"
]

vpc_azs = [
  "us-east-1a",
  "us-east-1b",
  "us-east-1c"
]

webapp_debug = 0
webapp_instances = 1

django_allowed_hosts = "*"
django_settings_module = "realworld.config.settings.base"
django_secret_key = "secret"
