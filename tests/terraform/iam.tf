

resource "aws_iam_user" "user_simple" {
  name = "b3d-test-user-simple"
}

resource "aws_iam_policy" "policy_simple" {
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "ec2:Describe*",
        ]
        Effect   = "Allow"
        Resource = "*"
      },
    ]
  })
}

resource "aws_iam_role" "role_simple" {
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_iam_policy" "user_composite_permissions_boundary_policy" {
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "ec2:Describe*",
        ]
        Effect   = "Allow"
        Resource = "*"
      },
    ]
  })
}

resource "aws_iam_user" "user_composite" {
  name = "b3d-test-user-composite-1"
  permissions_boundary = aws_iam_policy.user_composite_permissions_boundary_policy.arn
}

resource "aws_iam_access_key" "user_composite_access_key" {
  user = aws_iam_user.user_composite.name
}


resource "aws_iam_user_policy" "user_composite_policy" {
  name = "b3d-test-user-composite-policy"
  user = aws_iam_user.user_composite.name

  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Action" : [
          "ec2:Describe*"
        ],
        "Effect" : "Allow",
        "Resource" : "*"
      }
    ]
  })
}