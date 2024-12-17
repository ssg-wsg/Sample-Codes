# Define input variable for the secret value
variable "secret_value" {
  description = "The value of the secret to be stored"
  type        = string
  sensitive   = true
}

provider "aws" {
  region = "ap-southeast-1"
}

resource "aws_secretsmanager_secret" "example_secret" {
  name = "SampleApp/test" # Name of the secret
}

resource "aws_secretsmanager_secret_version" "example_secret_version" {
  secret_id     = aws_secretsmanager_secret.example_secret.id
  secret_string = json.encode({
    test_secret = var.secret_value
  })
}

