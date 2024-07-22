# adapted from https://blog.gruntwork.io/how-to-manage-terraform-state-28f5697e68fa

module "constants" {
  source = "../modules/constants"
}

provider "aws" {
  region = module.constants.AWS_REGION
}

# Provision a S3 bucket to store the Terraform state
resource "aws_s3_bucket" "tf_state" {
  bucket = module.constants.TF_BUCKET_NAME
  lifecycle {
    prevent_destroy = true
  }
}

# Enable Versioning to prevent accidental deletion
resource "aws_s3_bucket_versioning" "enabled" {
  bucket = aws_s3_bucket.tf_state.bucket
  versioning_configuration {
    status = "Enabled"
  }
}

# Enable server-side encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "default" {
  bucket = aws_s3_bucket.tf_state.bucket

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Block public access to the S3 bucket
resource "aws_s3_bucket_public_access_block" "public_access" {
  bucket                  = aws_s3_bucket.tf_state.bucket
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Create DynamoDB table for locking TF files
resource "aws_dynamodb_table" "tf_lock" {
  name         = module.constants.TF_DYNAMODB_TABLE_NAME
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}
