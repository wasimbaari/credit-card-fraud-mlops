variable "cluster_name" {
  description = "The name of the EKS cluster"
  type        = string
}

variable "subnet_ids" {
  description = "List of subnet IDs across multiple AZs for High Availability"
  type        = list(string)
}

variable "eks_role_arn" {
  description = "The ARN of the IAM role for the EKS Cluster control plane"
  type        = string
}

variable "node_role_arn" {
  description = "The ARN of the IAM role for the EKS Worker Nodes"
  type        = string
}