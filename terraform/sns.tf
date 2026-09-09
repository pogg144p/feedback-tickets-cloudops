# sns.tf
# ─────────────────────────────────────────────────────────────
# SNS + SQS ALERTING SYSTEM (Fan-Out Pattern)
#
# When a critical bug ticket is processed, the Loader Lambda
# publishes a message to SNS. SNS then "fans out" that message
# to ALL subscribers simultaneously:
#   1. Email subscription → instant email to your inbox
#   2. SQS Queue → stores the alert for audit trail / retry
#
# The SQS Queue also has a Dead Letter Queue (DLQ) — if a
# message fails processing 3 times, it moves to the DLQ
# instead of disappearing. Think of DLQ as the "lost & found"
# for messages.
#
# Fan-Out Pattern:
#   One publisher (Lambda) → One topic (SNS) → Many subscribers
#   This decouples the sender from the receivers. Lambda doesn't
#   need to know WHO gets the alert — it just publishes to SNS.
# ─────────────────────────────────────────────────────────────


# ── 1. SNS Topic ─────────────────────────────────────────────
# A "topic" is like a bulletin board. Anyone can pin a message
# to it, and everyone subscribed to it gets a copy.
resource "aws_sns_topic" "critical_alerts" {
  name = "${var.project_name}-critical-alerts-${var.environment}"

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}


# ── 2. SNS Email Subscription ────────────────────────────────
# Subscribe your email to the topic. AWS will send a
# confirmation email — you MUST click "Confirm subscription"
# or you won't receive any alerts.
resource "aws_sns_topic_subscription" "email_alert" {
  count     = var.alert_email != "" ? 1 : 0
  topic_arn = aws_sns_topic.critical_alerts.arn
  protocol  = "email"
  endpoint  = var.alert_email
}


# ── 3. SQS Queue (Message Buffer) ────────────────────────────
# The queue stores alert messages durably. Even if your email
# is down or you're offline, the message is safe in the queue.
# Messages are retained for 4 days (345600 seconds).
#
# redrive_policy = if a message fails 3 times, send it to the
# Dead Letter Queue instead of retrying forever.
resource "aws_sqs_queue" "alert_queue" {
  name                       = "${var.project_name}-alert-queue-${var.environment}"
  message_retention_seconds  = 345600 # 4 days
  visibility_timeout_seconds = 30     # how long a consumer has to process before retry
  receive_wait_time_seconds  = 10     # long polling (reduces API calls, saves cost)

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.alert_dlq.arn
    maxReceiveCount     = 3 # after 3 failures → move to DLQ
  })

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}


# ── 4. SQS Dead Letter Queue (DLQ) ───────────────────────────
# Safety net for failed messages. If a message can't be
# processed after 3 attempts, it lands here for investigation.
# Retained for 14 days so you have time to debug.
resource "aws_sqs_queue" "alert_dlq" {
  name                      = "${var.project_name}-alert-dlq-${var.environment}"
  message_retention_seconds = 1209600 # 14 days

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}


# ── 5. SNS → SQS Subscription ────────────────────────────────
# This subscribes the SQS queue to the SNS topic.
# Now when Lambda publishes to SNS, the message goes to BOTH
# your email AND this queue simultaneously (fan-out).
resource "aws_sns_topic_subscription" "sqs_alert" {
  topic_arn = aws_sns_topic.critical_alerts.arn
  protocol  = "sqs"
  endpoint  = aws_sqs_queue.alert_queue.arn
}


# ── 6. SQS Queue Policy ──────────────────────────────────────
# By default, SQS won't accept messages from SNS (security).
# This policy explicitly says: "Allow this specific SNS topic
# to send messages to this specific queue."
resource "aws_sqs_queue_policy" "allow_sns" {
  queue_url = aws_sqs_queue.alert_queue.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "sns.amazonaws.com" }
      Action    = "sqs:SendMessage"
      Resource  = aws_sqs_queue.alert_queue.arn
      Condition = {
        ArnEquals = {
          "aws:SourceArn" = aws_sns_topic.critical_alerts.arn
        }
      }
    }]
  })
}


# ── 7. IAM Policy — Allow Lambda to publish to SNS ───────────
# The Lambda execution role needs permission to call
# sns:Publish. This inline policy grants exactly that —
# nothing more (principle of least privilege).
resource "aws_iam_role_policy" "lambda_sns_publish" {
  name = "${var.project_name}-lambda-sns-publish-${var.environment}"
  role = aws_iam_role.lambda_exec.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = "sns:Publish"
      Resource = aws_sns_topic.critical_alerts.arn
    }]
  })
}
