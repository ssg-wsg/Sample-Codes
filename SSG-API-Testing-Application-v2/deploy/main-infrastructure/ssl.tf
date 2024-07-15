# Create SSL Certificates
variable "SSL_PRIVATE_KEY" {
  type = string
}

resource "tls_private_key" "private_key" {
  algorithm = "RSA"
  rsa_bits = 4096
}

resource "tls_self_signed_cert" "cert" {
  private_key_pem = var.SSL_PRIVATE_KEY

  subject {
    common_name = "api.testing.ssg"
    organization = "wsg-ssg"
  }

  validity_period_hours = 8760  # cert is valid for a year
  allowed_uses = [
    "key_encipherment",
    "digital_signature",
    "server_auth",
  ]
}

resource "aws_acm_certificate" "cert" {
  private_key = tls_private_key.private_key.private_key_pem
  certificate_body = tls_self_signed_cert.cert.cert_pem
}
