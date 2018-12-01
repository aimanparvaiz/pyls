module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "1.46.0"
  name = "${var.vpc_name}"
  cidr = "${var.vpc_cidr}"
  azs = "${var.azs}"
  private_subnets = "${var.private_subnets}"
  public_subnets = "${var.public_subnets}"
  tags = {
    Terraform = "true"
    Environment = "${var.env}"
  }
  enable_nat_gateway = true
}

output "vpc_id" {
  description = "The ID of the VPC"
  value       = "${module.vpc.vpc_id}"
}

output "private_subnets" {
  description = "Private subnet IDs"
  value = "${module.vpc.private_subnets}"

}
