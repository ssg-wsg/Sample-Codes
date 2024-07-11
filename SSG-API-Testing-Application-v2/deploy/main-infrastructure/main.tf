# Contains the main configurations for Terraform
module "constants" {
  source = "../modules/constants"
}

terraform {
  backend "s3" {
    bucket         = "ssg-tf-bucket"           # module.constants.TF_BUCKET_NAME
    key            = "main/main_infra.tfstate" # module.constants.TF_MAIN_BUCKET_FILE_KEY
    region         = "ap-southeast-1"          # module.constants.AWS_REGION
    dynamodb_table = "ssg-tf-state-lock"       # module.constants.TF_DYNAMODB_TABLE_NAME
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
  region = module.constants.AWS_REGION
}

# Create key pair for SSH into Bastion Host
resource "aws_key_pair" "default" {
  key_name   = "${module.constants.namespace}_keyPair"
  public_key = module.constants.ssh_public_key
}
