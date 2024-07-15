# Create SSL Certificates
variable "SSL_PRIVATE_KEY" {
  type = string
}

resource "tls_private_key" "private_key" {
  algorithm = "RSA"
  rsa_bits = 2048
}

resource "tls_self_signed_cert" "cert" {
  key_algorithm = tls_private_key.private_key.algorithm
  private_key_pem = SSL_PRIVATE_KEY

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
