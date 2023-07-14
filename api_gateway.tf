resource "aws_api_gateway_rest_api" "sms_api" {
  name        = "sms_api"
  description = "API Gateway for SMS processing"
}

resource "aws_api_gateway_resource" "sms_resource" {
  rest_api_id = aws_api_gateway_rest_api.sms_api.id
  parent_id   = aws_api_gateway_rest_api.sms_api.root_resource_id
  path_part   = "sms_processor"
}

resource "aws_api_gateway_method" "post_method" {
  rest_api_id   = aws_api_gateway_rest_api.sms_api.id
  resource_id   = aws_api_gateway_resource.sms_resource.id
  http_method   = "ANY"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda_integration" {
  rest_api_id             = aws_api_gateway_rest_api.sms_api.id
  resource_id             = aws_api_gateway_resource.sms_resource.id
  http_method             = aws_api_gateway_method.post_method.http_method
  integration_http_method = "ANY"
  type                    = "AWS"
  uri                     = aws_lambda_function.sms_processor.invoke_arn
}

resource "aws_api_gateway_method_response" "method_response" {
  rest_api_id = aws_api_gateway_rest_api.sms_api.id
  resource_id = aws_api_gateway_resource.sms_resource.id
  http_method = aws_api_gateway_method.post_method.http_method
  status_code = "200"
}

resource "aws_api_gateway_integration_response" "integration_response" {
  rest_api_id           = aws_api_gateway_rest_api.sms_api.id
  resource_id           = aws_api_gateway_resource.sms_resource.id
  http_method           = aws_api_gateway_method.post_method.http_method
  status_code           = aws_api_gateway_method_response.method_response.status_code
  response_templates = {
    "application/json" = ""
  }
}

resource "aws_api_gateway_deployment" "deployment" {
  depends_on    = [aws_api_gateway_integration.lambda_integration]
  rest_api_id   = aws_api_gateway_rest_api.sms_api.id
  stage_name    = "prod"
  variables = {
    lambdaAlias = aws_lambda_function.sms_processor.id
  }
}

output "api_endpoint" {
  value = aws_api_gateway_deployment.deployment.invoke_url
}
