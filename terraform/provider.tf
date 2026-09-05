# provider.tf
# ─────────────────────────────────────────────────────────────
# Terraform AWS Provider & Remote S3 Backend Configuration
#
# By storing state in S3, both your local machine and GitHub Actions
# CI/CD runners share the exact same state file in the cloud.
# ─────────────────────────────────────────────────────────────

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  required_version = ">= 1.3.0"

  # Remote S3 Backend — Shared state for Local + GitHub Actions CI/CD
  backend "s3" {
    bucket = "feedback-tickets-tfstate-768229077155"
    key    = "terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = var.aws_region
}
