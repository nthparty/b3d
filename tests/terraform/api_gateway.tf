
resource "aws_api_gateway_rest_api" "rest_api_simple" {
  name = "rest_api_simple"
}

resource "aws_api_gateway_usage_plan" "usage_plan_simple" {
  name = "usage_plan_simple"
}

resource "aws_api_gateway_api_key" "api_key_simple" {
  name = "api_key_simple"
}
