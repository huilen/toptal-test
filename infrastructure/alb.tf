resource "aws_security_group" "alb_security_group"{
  name = "${var.namespace}-${terraform.workspace}-webapp-alb-sg"
  vpc_id = module.vpc.vpc_id

  ingress {
    from_port = 80
    to_port = 80
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port = 0
    to_port = 0
    protocol = -1
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_lb" "load_balancer" {
  name = "${var.namespace}-${terraform.workspace}-webapp-alb"
  load_balancer_type = "application"
  internal = false
  security_groups = [aws_security_group.alb_security_group.id]
  subnets = module.vpc.public_subnets
  idle_timeout = 240
}

resource "aws_lb_listener" "lb_listener" {
  load_balancer_arn = aws_lb.load_balancer.arn
  port              = 80
  protocol          = "HTTP"
  default_action {
    type = "forward"
    target_group_arn = aws_lb_target_group.target_group.arn
  }
}

resource "aws_lb_target_group" "target_group" {
  name = "${var.namespace}-${terraform.workspace}-webapp-tg"
  port = 80
  protocol = "HTTP"
  vpc_id = module.vpc.vpc_id
  target_type = "instance"
  deregistration_delay = 10

  stickiness {
    enabled = true
    type = "lb_cookie"
  }

  health_check {
    port = 80
    path = "/"
    matcher = "200-499"
    healthy_threshold = 3
    interval = 300
    timeout = 120
  }

  lifecycle {
    create_before_destroy = true
  }

  depends_on = [aws_lb.load_balancer]
}
