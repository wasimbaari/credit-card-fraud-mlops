terraform {
  required_version = ">= 1.5.0"

  backend "s3" {
    bucket         = "fraud-mlops-tf-state"
    key            = "eks/terraform.tfstate"
    region         = "ap-south-1"
    dynamodb_table = "tf-lock"
  }
}

provider "aws" {
  region = var.region
}

# 1. VPC Module (Refactored for Multi-AZ/NAT Gateway)
module "vpc" {
  source       = "./modules/vpc"
  # Passing variables to avoid hardcoding inside the module
  vpc_cidr     = "10.0.0.0/16"
  project_name = "fraud-mlops"
  cluster_name = var.cluster_name
}

# 2. IAM Module (Handles all security roles)
module "iam" {
  source = "./modules/iam"
}

# 3. EKS Module (The final piece)
module "eks" {
  source       = "./modules/eks"
  cluster_name = var.cluster_name
  
  # DevSecOps: Pass the list of all subnets (Public + Private) for HA
  # This uses the outputs from your VPC module
  subnet_ids   = concat(module.vpc.public_subnet_ids, module.vpc.private_subnet_ids)
  
  # Pass ARNs from IAM module outputs
  eks_role_arn  = module.iam.eks_cluster_role_arn
  node_role_arn = module.iam.eks_node_role_arn
}