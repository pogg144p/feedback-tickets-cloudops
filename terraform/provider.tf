# provider.tf
# ─────────────────────────────────────────────────────────────
# Terraform AWS Provider Configuration
#
# When running locally, you can set the AWS_PROFILE environment variable.
# In CI/CD (GitHub Actions), credentials are automatically read
# from GitHub Secrets via standard AWS environment variables.
# ─────────────────────────────────────────────────────────────

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  required_version = ">= 1.3.0"
}

provider "aws" {
  region = var.aws_region
}
