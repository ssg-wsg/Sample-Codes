# Create SSL Certificates
variable "SSL_PRIVATE_KEY" {
  type = string
}

variable "SSL_PUBLIC_CERT" {
  type = string
}

resource "aws_acm_certificate" "cert" {
  private_key      = var.SSL_PRIVATE_KEY
  certificate_body = var.SSL_PUBLIC_CERT
}
