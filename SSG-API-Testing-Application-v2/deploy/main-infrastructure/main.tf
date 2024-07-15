# Contains the main configurations for Terraform
module "constants" {
  source = "../modules/constants"
}

terraform {
  backend "s3" {
    bucket         = "ssg-tf-bucket"
    key            = "main/main_infra.tfstate"
    region         = "ap-southeast-1"
    dynamodb_table = "ssg-tf-state-lock"
    encrypt        = true
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws",
      version = "5.17.0"
    }
  }
}

provider "aws" {
  region = module.constants.aws_region
}

# Create key pair for SSH into Bastion Host
resource "aws_key_pair" "default" {
  key_name   = "${module.constants.namespace}_keyPair"
  public_key = module.constants.ssh_public_key
}
