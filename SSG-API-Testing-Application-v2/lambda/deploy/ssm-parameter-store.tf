# Define input variables for the secret value, 
# env variable should have key value pairs like below
# {
#   "db_password": {
#     "value": "${{ secrets.DB_PASSWORD }}",
#     "description": "The database password for the application"
#   },
#   "api_key": {
#     "value": "${{ secrets.API_KEY }}",
#     "description": "The API key for accessing external services"
#   }
# }

variable "secrets" {
  description = "A map of secrets with their values and descriptions"
  type = map(object({
    value       = string
    description = string
  }))
  sensitive = true
}

resource "aws_ssm_parameter" "secrets" {
  for_each = var.secrets

  name        = each.key
  value       = each.value.value
  description = each.value.description

  type = "SecureString"
}

provider "aws" {
  region = "ap-southeast-1"
}
