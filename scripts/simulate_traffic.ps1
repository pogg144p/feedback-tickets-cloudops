# scripts/simulate_traffic.ps1
# ─────────────────────────────────────────────────────────────
# Live Traffic Simulation Script
#
# Generates realistic feedback tickets, uploads them to S3,
# and pushes live observability metrics to Prometheus & Grafana.
# Run this before an interview to demo a live, active pipeline!
# ─────────────────────────────────────────────────────────────

param (
    [int]$Count = 10,
    [string]$Profile = "tickets",
    [string]$PushgatewayUrl = "http://localhost:9091"
)

$ErrorActionPreference = "Stop"

Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "   🚀 Feedback Tickets Traffic Simulator            " -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan

# Sample realistic tickets
$SampleTickets = @(
    @{ User = "Alex Rivera"; Email = "alex@company.com"; Issue = "Critical bug: payment checkout button crashes on iOS"; Severity = "high"; Category = "bug"; Priority = "high" },
    @{ User = "Elena Rostova"; Email = "elena@tech.io"; Issue = "Please add dark mode and customizable keyboard shortcuts"; Severity = "low"; Category = "feature"; Priority = "low" },
    @{ User = "Marcus Chen"; Email = "marcus@dev.net"; Issue = "App response time is very slow and unresponsive during peak hours"; Severity = "medium"; Category = "complaint"; Priority = "medium" },
    @{ User = "Sophia Taylor"; Email = "sophia@web.org"; Issue = "How do I export my monthly data reports to CSV format?"; Severity = "low"; Category = "question"; Priority = "low" },
    @{ User = "Liam O'Connor"; Email = "liam@finance.co"; Issue = "Urgent: 2FA login verification code is not being delivered"; Severity = "high"; Category = "bug"; Priority = "high" },
    @{ User = "Maya Patel"; Email = "maya@cloud.ai"; Issue = "Would love to see a webhook integration for Slack notifications"; Severity = "low"; Category = "feature"; Priority = "low" },
    @{ User = "Noah Wilson"; Email = "noah@startup.io"; Issue = "Terrible experience with billing invoice generation failure"; Severity = "high"; Category = "complaint"; Priority = "high" },
    @{ User = "Zoe Martin"; Email = "zoe@design.com"; Issue = "Where can I find API documentation for custom webhooks?"; Severity = "low"; Category = "question"; Priority = "low" }
)

# Fetch account ID dynamically
$AccountId = aws sts get-caller-identity --profile $Profile --query "Account" --output text
$RawBucket = "feedback-tickets-raw-dev-$AccountId"

Write-Host "`n[1/2] Dropping simulated tickets into S3: s3://$RawBucket..." -ForegroundColor Yellow

$TotalSent = 0

for ($i = 1; $i -le $Count; $i++) {
    $Sample = $SampleTickets[$i % $SampleTickets.Count]
    $Timestamp = (Get-Date).ToString("yyyyMMdd-HHmmss")
    $Filename = "ticket_sim_${Timestamp}_$i.json"
    $TempPath = Join-Path $env:TEMP $Filename

    # Create ticket JSON
    $TicketJson = @{
        user      = $Sample.User
        email     = $Sample.Email
        issue     = $Sample.Issue
        severity  = $Sample.Severity
        simulated = $true
    } | ConvertTo-Json

    Set-Content -Path $TempPath -Value $TicketJson

    # Upload to S3
    aws s3 cp $TempPath "s3://$RawBucket/$Filename" --profile $Profile --quiet
    Remove-Item $TempPath -Force

    # Push Metric to Pushgateway
    $MetricUri = "$PushgatewayUrl/metrics/job/ticket_pipeline/category/$($Sample.Category)/priority/$($Sample.Priority)"
    try {
        Invoke-RestMethod -Uri $MetricUri -Method Post -Body "tickets_processed_total 1`n" -ErrorAction SilentlyContinue
    } catch {
        # Silent if local monitoring stack is offline
    }

    Write-Host "  ✔ Processed: [$($Sample.Category.ToUpper())] $($Sample.User) - Priority: $($Sample.Priority)" -ForegroundColor Green
    $TotalSent++
    Start-Sleep -Milliseconds 400
}

Write-Host "`n=====================================================" -ForegroundColor Cyan
Write-Host "  🎉 Sent $TotalSent tickets! Check DynamoDB & Grafana!" -ForegroundColor Cyan
Write-Host "  • Grafana Dashboard: http://localhost:3000          " -ForegroundColor Cyan
Write-Host "=====================================================`n" -ForegroundColor Cyan
