locals {
  launch_type   = "FARGATE"
  containerPort = 8094
}

resource "aws_ecs_cluster" "this" {
  name = "${var.application_name}_cluster"

}

resource "aws_iam_role" "ESCServiceRole" {
  name = "${var.application_name}_ECSServiceRole"
  assume_role_policy = jsonencode(
    {
      "Version" : "2012-10-17",
      "Statement" : [
        {
          "Effect" : "Allow",
          "Principal" : {
            "Service" : "ecs-tasks.amazonaws.com"
          },
          "Action" : "sts:AssumeRole"
        }
      ]
    }
  )

}

resource "aws_iam_policy_attachment" "taskexecutioAWSmanaged" {
  name       = "policy_atachment"
  roles      = ["${aws_iam_role.ESCServiceRole.name}"]
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}


resource "aws_iam_policy" "this" {
  name        = "${var.application_name}_ECSTaskExecution"
  description = "Policy for task def execution in ECS"

  # Terraform's "jsonencode" function converts a
  # Terraform expression result to valid JSON syntax.
  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Action" : [
          "s3:GetBucket*",
          "s3:GetObject*",
          "s3:List*"
        ],
        "Resource" : [
          "arn:aws:s3:::lambda-github-actions-test-bucket",
          "arn:aws:s3:::lambda-github-actions-test-bucket/*"
        ],
        "Effect" : "Allow",
        "Sid" : "AllowWriteByCiCdPolicy"
      },
      {
        "Action" : [
          "ecr:BatchCheckLayerAvailability",
          "ecr:BatchGetImage",
          "ecr:GetDownloadUrlForLayer"
        ],
        "Resource" : "${data.aws_ecr_repository.this.arn}",
        "Effect" : "Allow"
      },
      {
        "Action" : "ecr:GetAuthorizationToken",
        "Resource" : "*",
        "Effect" : "Allow"
      },
      {
        "Action" : [
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        "Resource" : "arn:aws:logs:eu-central-1:501280619881:log-group:cdkdashapp:*",
        "Effect" : "Allow"
      }
    ]
    }


  )
}

resource "aws_iam_role_policy_attachment" "taskexecutioncustom" {
  role       = aws_iam_role.ESCServiceRole.name
  policy_arn = aws_iam_policy.this.arn
}



resource "aws_ecs_task_definition" "this" {

  container_definitions = jsonencode([
    {
      name      = "${var.application_name}_container"
      image     = "${data.aws_ecr_repository.this.repository_url}:latest"
      cpu       = 10
      memory    = 512
      essential = true
      portMappings = [
        {
          containerPort = local.containerPort
        }
      ]
    }
    ]
  )
  task_role_arn            = aws_iam_role.ESCServiceRole.arn
  execution_role_arn       = aws_iam_role.ESCServiceRole.arn
  family                   = "${var.application_name}_taskdefinition"
  requires_compatibilities = [local.launch_type]

  cpu          = "256"
  memory       = "512"
  network_mode = "awsvpc"

}


resource "aws_security_group" "alb" {
  name   = "${var.application_name}_lb_securityGroup"
  vpc_id = data.aws_vpc.this.id

  ingress {
    protocol         = "tcp"
    from_port        = 80
    to_port          = 80
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  ingress {
    protocol         = "tcp"
    from_port        = local.containerPort
    to_port          = local.containerPort
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  egress {
    protocol         = "-1"
    from_port        = 0
    to_port          = 0
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

}



resource "aws_security_group" "fargate" {
  name   = "${var.application_name}_fargate_securityGroup"
  vpc_id = data.aws_vpc.this.id


  ingress {
    protocol         = "tcp"
    from_port        = local.containerPort
    to_port          = local.containerPort
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

}



resource "aws_lb" "this" {
  name               = "${var.application_name}LoadBalancer"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = data.aws_subnets.this.ids

  enable_deletion_protection = false
}


resource "aws_lb_target_group" "this" {
  name        = "${var.application_name}TargetGroup"
  port        = "80"
  protocol    = "HTTP"
  vpc_id      = data.aws_vpc.this.id
  target_type = "ip"



  health_check {
    healthy_threshold   = "3"
    interval            = "30"
    protocol            = "HTTP"
    matcher             = "200"
    timeout             = "3"
    path                = "/health"
    unhealthy_threshold = "2"
  }
  # depends_on = [aws_lb.this]

}



resource "aws_alb_listener" "http" {
  load_balancer_arn = aws_lb.this.arn
  port              = 80
  protocol          = "HTTP"





  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.this.arn

  }
}



resource "aws_ecs_service" "this" {
  name        = "${var.application_name}_service"
  cluster     = aws_ecs_cluster.this.arn
  launch_type = local.launch_type

  deployment_maximum_percent         = 200
  deployment_minimum_healthy_percent = 0
  desired_count                      = 1
  task_definition                    = "${aws_ecs_task_definition.this.family}:${aws_ecs_task_definition.this.revision}"
  health_check_grace_period_seconds  = 30



  load_balancer {
    # load_balancer_arn = aws_lb.this.arn
    target_group_arn = aws_lb_target_group.this.arn
    container_name   = "${var.application_name}_container"
    container_port   = local.containerPort


  }

  network_configuration {
    assign_public_ip = true
    security_groups  = [aws_security_group.alb.id]
    subnets          = data.aws_subnets.this.ids
  }


}
