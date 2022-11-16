locals {
  application_name = "dashapptf"
  launch_type      = "FARGATE"
  containerPort     = 8094
}

resource "aws_ecs_cluster" "this" {
  name = "${local.application_name}_cluster"

}


resource "aws_ecs_task_definition" "this" {

  container_definitions = jsonencode([
    {
      name      = "${local.application_name}_container"
      image     = "501280619881.dkr.ecr.eu-central-1.amazonaws.com/cdk-dashapp-repo:latest"
      cpu       = 10
      memory    = 512
      essential = true
      portMappings = [
        {
          containerPort = locals.containerPort
        }
      ]
    }
    ]
  )
  task_role_arn            = "arn:aws:iam::501280619881:role/ecsTaskExecutionRole"
  execution_role_arn       = "arn:aws:iam::501280619881:role/ecsTaskExecutionRole"
  family                   = "${local.application_name}_taskdefinition"
  requires_compatibilities = [local.launch_type]

  cpu          = "256"
  memory       = "512"
  network_mode = "awsvpc"

}

resource "aws_ecs_service" "this" {
  name        = "${local.application_name}_service"
  cluster     = aws_ecs_cluster.this.arn
  launch_type = local.launch_type

  deployment_maximum_percent         = 200
  deployment_minimum_healthy_percent = 0
  desired_count                      = 1
  task_definition                    = "${aws_ecs_task_definition.this.family}:${aws_ecs_task_definition.this.revision}"

  network_configuration {

    assign_public_ip = true
    security_groups  = data.aws_security_groups.this.ids
    subnets          = data.aws_subnet_ids.this.ids
  }


}
