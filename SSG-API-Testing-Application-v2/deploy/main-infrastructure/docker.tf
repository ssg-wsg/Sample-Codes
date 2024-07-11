# Create the Docker Image and push to ECR
locals {
  repo_url = aws_ecr_repository.ecr.repository_url
  hash     = md5(join("-", [for x in fileset("", "../../app/{*.py, Dockerfile}") : filemd5(x)]))
}

resource "null_resource" "image" {
  triggers = {
    hash = md5(join("-", [for x in fileset("", "../../app/{*.py, Dockerfile}") : filemd5(x)]))
  }

  provisioner "local-exec" {
    command = <<EOF
      aws ecr get-login-password | docker login --username AWS --password-stdin ${local.repo_url}
      docker build --platform linux/amd64 -t ${local.repo_url}:${local.hash} ../../app/
      docker push ${local.repo_url}:${local.hash}
    EOF
  }
}
