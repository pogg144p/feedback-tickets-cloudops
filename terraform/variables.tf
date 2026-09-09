# variables.tf
# ─────────────────────────────────────────────────────────────
# Variables are like function parameters for your infrastructure.
# Instead of hardcoding values like "us-east-1" everywhere,
# you define them once here and reuse them across all files.
#
# This means if you ever want to change the region, you change
# it in ONE place — not in 10 different files.
# ─────────────────────────────────────────────────────────────

variable "aws_region" {
  description = "The AWS region where all resources will be created"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "A prefix added to every resource name so you can identify them easily in AWS console"
  type        = string
  default     = "feedback-tickets"
}

variable "environment" {
  description = "The environment tag (dev, staging, prod) — we use dev for now"
  type        = string
  default     = "dev"
}

# ── Alerting Variables ─────────────────────────────────────────

variable "alert_email" {
  description = "Email address to receive critical bug alerts via SNS"
  type        = string
  default     = ""
}

variable "telegram_bot_token" {
  description = "Telegram Bot API token (from @BotFather) for instant push alerts"
  type        = string
  default     = ""
  sensitive   = true # won't be shown in terraform plan output
}

variable "telegram_chat_id" {
  description = "Your Telegram chat ID (the bot sends alerts to this chat)"
  type        = string
  default     = ""
}
