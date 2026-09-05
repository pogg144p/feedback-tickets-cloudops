# main.tf
# ─────────────────────────────────────────────────────────────
# This is where you actually DEFINE your AWS infrastructure.
# Each "resource" block = one thing Terraform will create on AWS.
#
# Week 1 creates 3 things:
#   1. S3 bucket → where raw tickets (JSON files) get dropped
#   2. S3 bucket → where processed tickets get stored
#   3. DynamoDB table → final database for queried ticket records
# ─────────────────────────────────────────────────────────────


# ── 1. S3 Bucket: Raw Tickets ────────────────────────────────
# This is the "inbox" — when someone submits a ticket,
# a JSON file lands here. Lambda will watch this bucket.
resource "aws_s3_bucket" "raw_tickets" {
  bucket = "${var.project_name}-raw-${var.environment}-${data.aws_caller_identity.current.account_id}"
  # ↑ S3 bucket names must be GLOBALLY unique across all of AWS.
  #   We add the account ID at the end to guarantee uniqueness.

  tags = {
    Name        = "Raw Tickets Bucket"
    Environment = var.environment
    Project     = var.project_name
  }
}

# Block all public access to raw bucket — tickets are private data
resource "aws_s3_bucket_public_access_block" "raw_tickets" {
  bucket = aws_s3_bucket.raw_tickets.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}


# ── 2. S3 Bucket: Processed Tickets ─────────────────────────
# After Lambda transforms the raw ticket, the cleaned version
# gets stored here as an archive/backup.
resource "aws_s3_bucket" "processed_tickets" {
  bucket = "${var.project_name}-processed-${var.environment}-${data.aws_caller_identity.current.account_id}"

  tags = {
    Name        = "Processed Tickets Bucket"
    Environment = var.environment
    Project     = var.project_name
  }
}

resource "aws_s3_bucket_public_access_block" "processed_tickets" {
  bucket = aws_s3_bucket.processed_tickets.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}


# ── 3. DynamoDB Table: Tickets ────────────────────────────────
# This is the final queryable database.
# After a ticket is processed, its record lives here.
# You can query: "show me all HIGH priority tickets today"
resource "aws_dynamodb_table" "tickets" {
  name         = "${var.project_name}-table-${var.environment}"
  billing_mode = "PAY_PER_REQUEST"
  # ↑ PAY_PER_REQUEST = free tier friendly.
  #   You only pay per read/write. With low traffic = $0.

  hash_key = "ticket_id"
  # ↑ This is the PRIMARY KEY — every ticket needs a unique ID.
  #   Think of it like the "id" column in a SQL table.

  attribute {
    name = "ticket_id"
    type = "S" # S = String type
  }

  tags = {
    Name        = "Tickets Table"
    Environment = var.environment
    Project     = var.project_name
  }
}


# ── Data Source: Get Current Account ID ──────────────────────
# This fetches your AWS account ID automatically.
# We use it to make S3 bucket names globally unique (above).
# It's not a resource — it just READS existing info from AWS.
data "aws_caller_identity" "current" {}
