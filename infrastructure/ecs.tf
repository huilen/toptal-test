resource "aws_ecs_cluster" "ecs_cluster" {
  name = "${var.namespace}-${terraform.workspace}"
  setting {
    name  = "containerInsights"
    value = "enabled"
  }
  
}

resource "aws_ecs_task_definition" "task_definition" {
  family = "${var.namespace}-${terraform.workspace}-webapp-task-definition"
  volume {
    name = "data"
  }
  container_definitions = templatefile("ecs-task-definition.json", merge({
    "namespace" = var.namespace,
    "env" = terraform.workspace,
    "region" = var.region,
    "log_group_name" = aws_cloudwatch_log_group.log_group.name,
    "webapp_port" = var.webapp_port,
    "config" = var.config,
    "database_url" = aws_db_instance.database.address,
    "database_port" = aws_db_instance.database.port,
    "database_name" = aws_db_instance.database.name,
    "database_username" = aws_db_instance.database.username,
    "database_password" = aws_db_instance.database.password,
    "webapp_debug" = var.webapp_debug,
    "account_id" = data.aws_caller_identity.current.account_id
    "django_allowed_hosts" = var.django_allowed_hosts,
    "django_settings_module" = var.django_settings_module,
    "django_secret_key" = var.django_secret_key
  }))
  volume {
    name = "static_volume"
  }
  execution_role_arn = aws_iam_role.task_execution_role.arn
  task_role_arn = aws_iam_role.task_role.arn
  requires_compatibilities = ["EC2"]
  network_mode = "bridge"
}

resource "aws_ecs_service" "ecs_service" {
  name = "webapp"
  cluster = aws_ecs_cluster.ecs_cluster.id
  task_definition = aws_ecs_task_definition.task_definition.arn
  desired_count = var.webapp_instances
  launch_type = "EC2"
  enable_execute_command = true
  
  load_balancer {
    target_group_arn = aws_lb_target_group.target_group.arn
    container_name = "nginx"
    container_port = 80
  }
}

resource "aws_iam_role" "task_role" {
  name = "${var.namespace}-${terraform.workspace}-webapp-ecs-task-role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "ecs-tasks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_cloudwatch_log_group" "log_group" {
  name = "${var.namespace}/${terraform.workspace}/webapp"
  retention_in_days = 3
}

resource "aws_iam_role" "task_execution_role" {
  name = "${var.namespace}-${terraform.workspace}-webapp-ecs-task-execution-role"

  assume_role_policy = <<EOF
{
    "Version": "2012-10-17",    "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "ecs-tasks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "ecs_task_execution_role_policy" {
  name = "${var.namespace}-${terraform.workspace}-webapp-ecs-task-execution-role-policy"
  role = aws_iam_role.task_execution_role.id
  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
      {
          "Effect": "Allow",
          "Action": [
              "logs:CreateLogGroup",
              "logs:CreateLogStream",
              "logs:PutLogEvents",
              "logs:DescribeLogStreams"
          ],
          "Resource": [
              "arn:aws:logs:*:*:*"
          ]
      },
      {
        "Effect": "Allow",
        "Action": [
          "secretsmanager:GetSecretValue"
        ],
        "Resource": [
          "arn:aws:secretsmanager:${var.region}:${data.aws_caller_identity.current.account_id}:secret:*"
        ]
      },
      {
          "Effect": "Allow",
          "Action": [
              "ssm:GetParametersByPath",
              "ssm:GetParameters",
              "ssm:GetParameter"
          ],
          "Resource": "arn:aws:ssm:*:*:parameter/*"
      },
      {
            "Effect": "Allow",
            "Action": [
                "ecr:GetDownloadUrlForLayer",
                "ecr:BatchGetImage",
                "ecr:DescribeImages",
                "ecr:GetAuthorizationToken",
                "ecr:BatchCheckLayerAvailability"
            ],
            "Resource": "*"
      }
    ]
}
EOF
}

resource "aws_security_group" "service_security_group" {
  name = "${var.namespace}-${terraform.workspace}-webapp-service-sg"
  vpc_id = module.vpc.vpc_id
  ingress {
    from_port = 80
    protocol = "tcp"
    to_port = 80
    cidr_blocks = ["0.0.0.0/0"] # should be alb sg
  }
  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
}

data "aws_iam_policy_document" "ecs_agent" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "ecs_agent" {
  name               = "ecs-agent"
  assume_role_policy = data.aws_iam_policy_document.ecs_agent.json
}


resource "aws_iam_role_policy_attachment" "ecs_agent" {
  role       = aws_iam_role.ecs_agent.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role"
}

resource "aws_iam_instance_profile" "ecs_agent" {
  name = "ecs-agent"
  role = aws_iam_role.ecs_agent.name
}

resource "aws_launch_configuration" "ecs_instance_config" {
  name_prefix                 = "${var.namespace}-${terraform.workspace}-webapp-"
  image_id                    = "ami-04ca8c64160cd4188"
  instance_type = "t2.micro"
  lifecycle {
    create_before_destroy = true
  }
  user_data = <<EOF
#!/bin/bash
echo ECS_CLUSTER=${aws_ecs_cluster.ecs_cluster.name} >> /etc/ecs/ecs.config
EOF

  iam_instance_profile        = aws_iam_instance_profile.ecs_agent.arn
  security_groups             = [aws_security_group.service_security_group.id]
}

resource "aws_autoscaling_group" "ecs_ag" {
  name_prefix = "${var.namespace}-${terraform.workspace}-webapp-ag"
  termination_policies = [
     "OldestInstance" 
  ]
  default_cooldown          = 30
  health_check_grace_period = 30
  max_size                  = 1
  min_size                  = 1
  desired_capacity          = 1

  vpc_zone_identifier       = module.vpc.private_subnets

  launch_configuration      = aws_launch_configuration.ecs_instance_config.name

  lifecycle {
    create_before_destroy   = true
  }
}
