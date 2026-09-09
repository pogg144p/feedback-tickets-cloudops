# lambda.tf
# ─────────────────────────────────────────────────────────────
# AWS Lambda Functions (Running as Docker Containers from ECR)
#
# In Week 3, we migrated from ZIP files to Container Images (Docker).
# Each function points to its respective AWS ECR repository image.
# ─────────────────────────────────────────────────────────────

# ── 1. IAM Role for Lambda Execution ──────────────────────────
resource "aws_iam_role" "lambda_exec" {
  name = "${var.project_name}-lambda-role-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}

# Attach managed permission policies to Lambda role
resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "lambda_s3" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_iam_role_policy_attachment" "lambda_dynamodb" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
}

resource "aws_iam_role_policy_attachment" "lambda_invoke" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/AWSLambda_FullAccess"
}


# ── 2a. Lambda: Extractor (Container Image) ───────────────────
resource "aws_lambda_function" "extractor" {
  function_name = "${var.project_name}-extractor-${var.environment}"
  role          = aws_iam_role.lambda_exec.arn

  # Package type Image tells AWS to use a Docker container
  package_type = "Image"
  image_uri    = "${aws_ecr_repository.extractor.repository_url}:latest"

  timeout     = 30
  memory_size = 128

  environment {
    variables = {
      TRANSFORMER_FUNCTION_NAME = "${var.project_name}-transformer-${var.environment}"
    }
  }

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}


# ── 2b. Lambda: Transformer (Container Image) ─────────────────
resource "aws_lambda_function" "transformer" {
  function_name = "${var.project_name}-transformer-${var.environment}"
  role          = aws_iam_role.lambda_exec.arn

  package_type = "Image"
  image_uri    = "${aws_ecr_repository.transformer.repository_url}:latest"

  timeout     = 30
  memory_size = 128

  environment {
    variables = {
      LOADER_FUNCTION_NAME = "${var.project_name}-loader-${var.environment}"
    }
  }

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}


# ── 2c. Lambda: Loader (Container Image) ──────────────────────
resource "aws_lambda_function" "loader" {
  function_name = "${var.project_name}-loader-${var.environment}"
  role          = aws_iam_role.lambda_exec.arn

  package_type = "Image"
  image_uri    = "${aws_ecr_repository.loader.repository_url}:latest"

  timeout     = 30
  memory_size = 128

  environment {
    variables = {
      DYNAMODB_TABLE_NAME   = aws_dynamodb_table.tickets.name
      PROCESSED_BUCKET_NAME = aws_s3_bucket.processed_tickets.bucket
      SNS_TOPIC_ARN         = aws_sns_topic.critical_alerts.arn
      TELEGRAM_BOT_TOKEN    = var.telegram_bot_token
      TELEGRAM_CHAT_ID      = var.telegram_chat_id
    }
  }

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}


# ── 3. S3 Trigger — connects raw bucket to Extractor Lambda ───
resource "aws_s3_bucket_notification" "raw_bucket_trigger" {
  bucket = aws_s3_bucket.raw_tickets.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.extractor.arn
    events              = ["s3:ObjectCreated:*"]
    filter_suffix       = ".json"
  }

  depends_on = [aws_lambda_permission.allow_s3_invoke]
}

resource "aws_lambda_permission" "allow_s3_invoke" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.extractor.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.raw_tickets.arn
}
