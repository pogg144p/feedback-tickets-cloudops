# outputs.tf
# ─────────────────────────────────────────────────────────────
# Outputs are values Terraform PRINTS to your terminal after
# a successful apply. Think of them as "what did we just create?"
#
# They're also useful in Week 2 — Lambda needs to know the S3
# bucket name to watch. Outputs make sharing values easy.
# ─────────────────────────────────────────────────────────────

output "raw_bucket_name" {
  description = "Name of the S3 bucket where raw ticket JSON files are dropped"
  value       = aws_s3_bucket.raw_tickets.bucket
}

output "processed_bucket_name" {
  description = "Name of the S3 bucket where processed tickets are archived"
  value       = aws_s3_bucket.processed_tickets.bucket
}

output "dynamodb_table_name" {
  description = "Name of the DynamoDB table storing final ticket records"
  value       = aws_dynamodb_table.tickets.name
}

output "aws_region" {
  description = "The AWS region everything was deployed into"
  value       = var.aws_region
}

# ── Alerting Outputs ───────────────────────────────────────────

output "sns_topic_arn" {
  description = "ARN of the SNS topic for critical bug alerts"
  value       = aws_sns_topic.critical_alerts.arn
}

output "sqs_queue_url" {
  description = "URL of the SQS queue storing alert messages"
  value       = aws_sqs_queue.alert_queue.url
}

output "sqs_dlq_url" {
  description = "URL of the Dead Letter Queue for failed alerts"
  value       = aws_sqs_queue.alert_dlq.url
}
