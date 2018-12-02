module "eks" {
  source = "terraform-aws-modules/eks/aws"
  version = "1.7.0"
  cluster_name = "${var.cluster_name}"
  vpc_id = "${var.vpc_id}"
  subnets = "${var.private_subnets}"
  tags = "${var.tags}"
  worker_groups = "${var.worker_groups}"
  worker_group_count = "${var.worker_group_count}"
  kubeconfig_name = "${var.kubeconfig_name}"
  config_output_path = "${var.config_output_path}"
}
output "cluster_certificate_authority_data" {
  value       = "${module.eks.cluster_certificate_authority_data}"
}

output "cluster_endpoint" {
  value       = "${module.eks.cluster_endpoint}"
}

output "cluster_id" {
  value       = "${module.eks.cluster_id}"
}
output "kubeconfig" {
  value       = "${module.eks.kubeconfig}"
}
output "worker_security_group_id" {
  value = "${module.eks.worker_security_group_id}"
}
