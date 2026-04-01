resource "aws_eks_cluster" "this" {
  name     = var.cluster_name
  role_arn = var.eks_role_arn  # <--- Use the variable here

  vpc_config {
    subnet_ids = var.subnet_ids
  }
}

resource "aws_eks_node_group" "this" {
  cluster_name    = aws_eks_cluster.this.name
  node_group_name = "${var.cluster_name}-nodes"
  node_role_arn   = var.node_role_arn # <--- Use the variable here
  subnet_ids      = var.subnet_ids

  scaling_config {
    desired_size = 2
    max_size     = 6
    min_size     = 1
  }
}