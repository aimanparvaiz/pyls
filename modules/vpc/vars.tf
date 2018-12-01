variable "vpc_name" {
  description = "Name of the vpc"
}
variable "vpc_cidr" {
  description = "VPC cidr"
}
variable "env" {
  description = "production, dev, qa, stage"
}

variable "public_subnets" {
  type = "list"
}

variable "private_subnets" {
  type = "list"
}

variable "azs" {
  type = "list"
}

variable "enable_dns_support" {
}


variable "enable_dns_hostnames" {
}
