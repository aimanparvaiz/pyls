variable "cluster_name" {
  description = "Cluster name"
}
variable "private_subnets" {
  type = "list"
  description = "List of subnet ids for nodes"
}
variable "tags" {
  type = "map"
  description = "AWS resource tags"
}
variable "vpc_id" {
  description = "VPC id for eks cluster"
}
variable "worker_group_count" {
  description = "worker groups count for eks cluster"
}
variable "worker_groups" {
  description = "A list of maps defining worker group configurations. See workers_group_defaults for valid keys."
  type        = "list"
}

