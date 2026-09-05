# provider.tf
# ─────────────────────────────────────────────────────────────
# This file tells Terraform TWO things:
#   1. Which cloud provider to use (AWS)
#   2. Which AWS credentials profile to use (our "tickets" profile)
#
# Think of this as the "login" file — before Terraform can create
# anything on AWS, it needs to know WHO it's logging in as.
# ─────────────────────────────────────────────────────────────

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws" # Download the official AWS plugin
      version = "~> 5.0"        # Use version 5.x (latest stable)
    }
  }

  required_version = ">= 1.3.0" # Minimum Terraform version needed
}

provider "aws" {
  region  = var.aws_region # Which AWS region to deploy into (defined in variables.tf)
  profile = "tickets"      # The AWS CLI profile we set up → feedback-tickets-user
}
