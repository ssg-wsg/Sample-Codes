# Create ECR repository
module "constants" {
  source = "../modules/constants"
}

terraform {
  backend "s3" {
    bucket         = "ssg-tf-bucket"
    key            = "main/ecr.tfstate"
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

resource "aws_ecr_repository" "ecr" {
  name                 = "${module.constants.namespace}/${module.constants.service_name}"
  force_delete         = false
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}
