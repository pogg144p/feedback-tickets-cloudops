# ecr.tf
# ─────────────────────────────────────────────────────────────
# AWS ECR (Elastic Container Registry)
#
# ECR is AWS's private Docker registry. We create 3 repositories:
#   1. feedback-tickets-extractor
#   2. feedback-tickets-transformer
#   3. feedback-tickets-loader
#
# Each repository will store the Docker image for that Lambda function.
# ─────────────────────────────────────────────────────────────

# ── 1. ECR Repo: Extractor ────────────────────────────────────
resource "aws_ecr_repository" "extractor" {
  name                 = "${var.project_name}-extractor"
  image_tag_mutability = "MUTABLE"

  # scan_on_push checks your images for known security vulnerabilities automatically
  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}

# ── 2. ECR Repo: Transformer ──────────────────────────────────
resource "aws_ecr_repository" "transformer" {
  name                 = "${var.project_name}-transformer"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}

# ── 3. ECR Repo: Loader ───────────────────────────────────────
resource "aws_ecr_repository" "loader" {
  name                 = "${var.project_name}-loader"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}

# ── Outputs for ECR Repository URLs ───────────────────────────
# Terraform will print these exact URLs so we know where to push our Docker images!
output "ecr_extractor_url" {
  description = "URL of the Extractor ECR repository"
  value       = aws_ecr_repository.extractor.repository_url
}

output "ecr_transformer_url" {
  description = "URL of the Transformer ECR repository"
  value       = aws_ecr_repository.transformer.repository_url
}

output "ecr_loader_url" {
  description = "URL of the Loader ECR repository"
  value       = aws_ecr_repository.loader.repository_url
}
