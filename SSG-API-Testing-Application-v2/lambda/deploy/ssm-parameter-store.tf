# Define input variable for the secret value
variable "secret_value" {
  description = "The value of the secret to be stored"
  type        = string
  sensitive   = true
}

provider "aws" {
  region = "ap-southeast-1"
}

resource "aws_ssm_parameter" "example_secret" {
  name        = "/SampleApp/example_secrets/example" # Name of the secret
  description = "The parameter description"
  type        = "SecureString"
  value       = var.secret_value
}
