# Contains the main configurations for Terraform
module "constants" {
  source = "../../modules/constants"
}

terraform {
  backend "s3" {
    bucket         = "ssg-tf-dev-bucket"           # module.constants.s3_dev_bucket_name
    key            = "main/infrastructure.tfstate" # module.constants.ecr_s3_state_bucket_name
    region         = "ap-southeast-1"              # module.constants.aws_region
    dynamodb_table = "ssg-terraform-state-lock"    # module.constants.dynamodb_table_name
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
  key_name   = "${module.constants.namespace}-key-pair"
  public_key = module.constants.ssh_public_key
}
