
resource "aws_ssm_parameter" "ssm_parameter_simple" {
  name      = "_ssm_parameter_simple"
  type      = "SecureString"
  value     = "test"
}