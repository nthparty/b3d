
resource "aws_iam_role" "iam_for_lambda" {
  assume_role_policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": "sts:AssumeRole",
        "Principal": {
          "Service": "lambda.amazonaws.com"
        },
        "Effect": "Allow",
        "Sid": ""
      }
    ]
  })
}

resource "aws_lambda_function" "lambda_function_simple" {
  filename      = "main.py.zip"
  function_name = "lambda_function_simple"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "main.handler"
  runtime       = "python3.8"
}