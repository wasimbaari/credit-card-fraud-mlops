resource "aws_eks_cluster" "this" {
  name     = var.cluster_name
  role_arn = var.eks_role_arn

  vpc_config {
    subnet_ids = var.subnet_ids
  }
}

resource "aws_eks_node_group" "this" {
  cluster_name    = aws_eks_cluster.this.name
  node_group_name = "${var.cluster_name}-nodes"
  node_role_arn   = var.node_role_arn
  subnet_ids      = var.subnet_ids

  # UPGRADE: Using t3.large (2 vCPU, 8GB RAM) to handle Istio + KServe overhead
  instance_types = ["t3.large"]

  # DEVSECOPS TIP: Use SPOT instances to save ~70% on your AWS bill. 
  # If a spot node is reclaimed, EKS will automatically spin up a new one.
  capacity_type  = "SPOT"

  scaling_config {
    # UPGRADE: Moving to 3 nodes to provide 6 vCPUs total cluster capacity
    desired_size = 3
    max_size     = 6
    min_size     = 1
  }

  # Ensure the cluster is established before creating nodes
  depends_on = [
    aws_eks_cluster.this
  ]
}