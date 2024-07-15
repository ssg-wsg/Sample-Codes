# Create ECR repository
module "constants" {
  source = "../modules/constants"
}

terraform {
  backend "s3" {
    bucket         = "ssg-tf-bucket"           # module.constants.TF_BUCKET_NAME
    key            = "main/ecr.tfstate"        # module.constants.TF_MAIN_BUCKET_FILE_KEY
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

resource "aws_ecr_repository" "ecr" {
  name                 = "${module.constants.namespace}/${module.constants.service_name}"
  force_delete         = false
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}
