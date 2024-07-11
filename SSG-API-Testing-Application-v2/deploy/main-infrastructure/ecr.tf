# Create ECR repository
resource "aws_ecr_repository" "ecr" {
  name                 = "${module.constants.namespace}/${module.constants.service_name}"
  force_delete         = false
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}
