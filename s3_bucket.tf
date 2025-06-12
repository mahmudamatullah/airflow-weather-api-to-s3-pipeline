resource "aws_s3_bucket" "amatullah_user" {
  bucket = "amatullah-data-bucket"

  tags = {
    Name        = "Mahmud_bucket"
  }
}

resource "aws_iam_user" "amatullah_demo" {
  name = "amatullah_user"
  path = "/system/"

  tags = {
    tag-key = "amatullah-value"
  }
}

resource "aws_iam_access_key" "amatullah_demo" {
  user = aws_iam_user.amatullah_demo.name
}

data "aws_iam_policy_document" "amatullah_policy1" {
  statement {
    effect    = "Allow"
    actions   = ["s3:PutObject"]
    resources = ["arn:aws:s3:::amatullah-data-bucket"]
  }
}

resource "aws_iam_user_policy" "amatullah_policy1" {
  name   = "ama_policy"
  user   = aws_iam_user.amatullah_demo.name
  policy = data.aws_iam_policy_document.amatullah_policy1.json
}

resource "aws_ssm_parameter" "ama_accesskey" {
  name  = "amatu_accesskey"
  type  = "SecureString"
  value =  aws_iam_access_key.amatullah_demo.id
}

resource "aws_ssm_parameter" "ama_secretkey" {
  name  = "amatu_secretkey"
  type  = "SecureString"
  value = aws_iam_access_key.amatullah_demo.secret
}