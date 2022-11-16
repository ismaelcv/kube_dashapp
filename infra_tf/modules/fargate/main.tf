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
      "Version" : "2008-10-17",
      "Statement" : [
        {
          "Sid" : "",
          "Effect" : "Allow",
          "Principal" : {
            "Service" : "ec2.amazonaws.com"
          },
          "Action" : "sts:AssumeRole"
        }
      ]
    }
  )

}

resource "aws_iam_policy_attachment" "this" {
  name       = "policy_atachment"
  roles      = ["${aws_iam_role.ESCServiceRole.name}"]
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role"
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

# resource "aws_ecs_service" "this" {
#   name        = "${var.application_name}_service"
#   cluster     = aws_ecs_cluster.this.arn
#   launch_type = local.launch_type

#   deployment_maximum_percent         = 200
#   deployment_minimum_healthy_percent = 0
#   desired_count                      = 1
#   task_definition                    = "${aws_ecs_task_definition.this.family}:${aws_ecs_task_definition.this.revision}"

#   network_configuration {

#     assign_public_ip = true
#     security_groups  = data.aws_security_groups.this.ids
#     subnets          = data.aws_subnets.this.ids
#   }


# }
