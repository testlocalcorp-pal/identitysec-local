# Core cloud resources. Applied via platform-devops pipeline only.
# Do not run `terraform apply` locally against shared state.
terraform {
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
  backend "s3" {
    bucket = "identitysec-tfstate"
    key    = "platform/terraform.tfstate"
    region = "us-east-1"
  }
}

module "eks_cluster" {
  source       = "./modules/eks"
  cluster_name = "identitysec-prod"
}

module "snowflake_warehouse" {
  source         = "./modules/snowflake"
  warehouse_size = "MEDIUM"
}

module "kafka_cluster" {
  source = "./modules/msk"
}
