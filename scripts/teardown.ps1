# scripts/teardown.ps1
# ─────────────────────────────────────────────────────────────
# Teardown Script — Zero Spend Guarantee
#
# Empties S3 buckets (Terraform cannot delete non-empty buckets)
# and runs 'terraform destroy' to remove all AWS resources.
# ─────────────────────────────────────────────────────────────

param (
    [string]$Profile = "tickets"
)

$ErrorActionPreference = "Continue"

Write-Host "=====================================================" -ForegroundColor Red
Write-Host "   ⚠️  FEEDBACK TICKETS PLATFORM TEARDOWN           " -ForegroundColor Red
Write-Host "=====================================================" -ForegroundColor Red

$Confirmation = Read-Host "Are you sure you want to destroy all AWS infrastructure? (type 'yes' to proceed)"
if ($Confirmation -ne "yes") {
    Write-Host "Teardown aborted." -ForegroundColor Yellow
    exit
}

# 1. Fetch account ID
$AccountId = aws sts get-caller-identity --profile $Profile --query "Account" --output text
$RawBucket = "feedback-tickets-raw-dev-$AccountId"
$ProcessedBucket = "feedback-tickets-processed-dev-$AccountId"

# 2. Empty S3 Buckets first
Write-Host "`n[1/3] Emptying S3 raw bucket: $RawBucket..." -ForegroundColor Yellow
aws s3 rm "s3://$RawBucket" --recursive --profile $Profile

Write-Host "`n[2/3] Emptying S3 processed bucket: $ProcessedBucket..." -ForegroundColor Yellow
aws s3 rm "s3://$ProcessedBucket" --recursive --profile $Profile

# 3. Run Terraform Destroy
Write-Host "`n[3/3] Running Terraform Destroy..." -ForegroundColor Yellow
$TerraformDir = Join-Path (Split-Path -Parent $PSScriptRoot) "terraform"
Push-Location $TerraformDir
$env:AWS_PROFILE = $Profile
terraform destroy -auto-approve
Pop-Location

# 4. Stop Docker Compose Monitoring
Write-Host "`nStopping local monitoring containers..." -ForegroundColor Yellow
$MonitoringDir = Join-Path (Split-Path -Parent $PSScriptRoot) "monitoring"
Push-Location $MonitoringDir
docker compose down
Pop-Location

Write-Host "`n=====================================================" -ForegroundColor Green
Write-Host "  ✔ All AWS & Local resources successfully destroyed! " -ForegroundColor Green
Write-Host "=====================================================" -ForegroundColor Green
