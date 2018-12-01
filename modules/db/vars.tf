variable "name" {
  description = "DB name"
}
variable "identifier" {
  description = "DB identifier"
}
variable "env" {
  description = "DB env"
}
variable "vpc_sg_id" {
  description = "SG id of the VPC"
  type = "list"
}
variable "vpc_subnets" {
  description = "VPC Subnets"
  type = "list"
}
