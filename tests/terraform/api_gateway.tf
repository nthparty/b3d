
resource "aws_api_gateway_rest_api" "rest_api_simple" {
  name        = "rest_api_simple"
}

resource "aws_api_gateway_usage_plan" "usage_plan_simple" {
  name        = "usage_plan_simple"
}

resource "aws_api_gateway_api_key" "api_key_simple" {
  name        = "api_key_simple"
}

resource "aws_api_gateway_rest_api" "rest_api_composite" {
  name        = "rest_api_composite"
}

resource "aws_api_gateway_method" "rest_api_composite_method_options" {
  rest_api_id = aws_api_gateway_rest_api.rest_api_composite.id
  resource_id = aws_api_gateway_rest_api.rest_api_composite.root_resource_id
  http_method = "OPTIONS"
  authorization = "NONE"
  api_key_required = false
  request_parameters = {}
}

resource "aws_api_gateway_method_response" "rest_api_composite_method_response_options" {
  http_method = aws_api_gateway_method.rest_api_composite_method_options.http_method
  resource_id = aws_api_gateway_rest_api.rest_api_composite.root_resource_id
  rest_api_id = aws_api_gateway_rest_api.rest_api_composite.id
  status_code = "200"
}

resource "aws_api_gateway_integration" "rest_api_composite_integration_options" {
  rest_api_id = aws_api_gateway_rest_api.rest_api_composite.id
  resource_id = aws_api_gateway_rest_api.rest_api_composite.root_resource_id
  http_method = aws_api_gateway_method.rest_api_composite_method_options.http_method
  type = "MOCK"
  request_templates = {
    "application/json" = "{'statusCode': 200}"
  }
  passthrough_behavior = "WHEN_NO_MATCH"
  timeout_milliseconds = 29000
  cache_namespace = aws_api_gateway_rest_api.rest_api_composite.root_resource_id
  cache_key_parameters = []
  depends_on = [
    aws_api_gateway_method.rest_api_composite_method_options
  ]
}

resource "aws_api_gateway_integration_response" "response_200_options" {
  rest_api_id = aws_api_gateway_rest_api.rest_api_composite.id
  resource_id = aws_api_gateway_rest_api.rest_api_composite.root_resource_id
  http_method = aws_api_gateway_method.rest_api_composite_method_options.http_method
  status_code = aws_api_gateway_method_response.rest_api_composite_method_response_options.status_code
  response_templates = {}
}

resource "aws_api_gateway_deployment" "rest_api_composite_deployment" {
  rest_api_id = aws_api_gateway_rest_api.rest_api_composite.id
  stage_name  = "rest_api_composite_stage"

  depends_on = [
    aws_api_gateway_method.rest_api_composite_method_options,
    aws_api_gateway_integration.rest_api_composite_integration_options
  ]
}

resource "aws_api_gateway_usage_plan" "usage_plan_composite" {
  name        = "usage_plan_composite"
  api_stages {
    api_id      = aws_api_gateway_rest_api.rest_api_composite.id
    stage       = "rest_api_composite_stage"
  }
  depends_on = [
    aws_api_gateway_deployment.rest_api_composite_deployment
  ]
}

resource "aws_api_gateway_api_key" "api_key_composite" {
  name          = "api_key_composite"
}

resource "aws_api_gateway_usage_plan_key" "usage_plan_key_composite" {
  key_id = aws_api_gateway_api_key.api_key_composite.id
  key_type = "API_KEY"
  usage_plan_id = aws_api_gateway_usage_plan.usage_plan_composite.id
}
