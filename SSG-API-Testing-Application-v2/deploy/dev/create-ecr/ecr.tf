# Create ECR repository
module "constants" {
  source = "../../modules/constants"
}

terraform {
  backend "s3" {
    bucket         = "ssg-tf-dev-bucket"        # module.constants.s3_dev_bucket_name
    key            = "main/ecr.tfstate"         # module.constants.ecr_s3_state_bucket_name
    region         = "ap-southeast-1"           # module.constants.aws_region
    dynamodb_table = "ssg-terraform-state-lock" # module.constants.dynamodb_table_name
    encrypt        = true
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws",
      version = "5.17.0"
    }
  }
}

resource "aws_ecr_repository" "ecr_repository" {
  name                 = "${module.constants.namespace}/${module.constants.service_name}"
  force_delete         = false
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  encryption_configuration {
    encryption_type = "AES256"
  }
}
