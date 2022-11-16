data "aws_vpc" "this" {
  default = true
} 

data "aws_subnet_ids" "this" {
  vpc_id = data.aws_vpc.this.id

}



data "aws_security_groups" "this" {

  filter {
    name   = "group-name"
    values = ["allow-tcp"]
  }

  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.this.id]
  }
}

