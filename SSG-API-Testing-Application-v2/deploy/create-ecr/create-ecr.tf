# Import constants
module "constants" {
  source = "../modules/constants"
}

# Specify dependencies
terraform {
  backend "s3" {
    bucket         = "ssg-tf-bucket"     # module.constants.TF_BUCKET_NAME
    key            = "ecr/ecr.tfstate"   # module.constants.TF_ECR_BUCKET_FILE_KEY
    region         = "ap-southeast-1"    # module.constants.AWS_REGION
    dynamodb_table = "ssg-tf-state-lock" # module.constants.TF_DYNAMODB_TABLE_NAME
    encrypt        = true
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws",
      version = "5.17.0"
    }
  }
}

# Define AWS as a provider
provider "aws" {
  region = module.constants.AWS_REGION
}

# Create ECS Service
resource "aws_ecr_repository" "app" {
  name                 = module.constants.ECR_REPO_NAME
  image_tag_mutability = "MUTABLE"
  force_delete         = true

  image_scanning_configuration {
    scan_on_push = false
  }
}

output "app_url" {
  value = aws_ecr_repository.app.repository_url
}
