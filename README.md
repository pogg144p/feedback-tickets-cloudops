# 🚀 Serverless CloudOps Ticket Analytics Platform

[![CI - Code Quality & Testing](https://github.com/pogg144p/feedback-tickets-cloudops/actions/workflows/ci.yml/badge.svg)](https://github.com/pogg144p/feedback-tickets-cloudops/actions/workflows/ci.yml)
[![CD - Build & Deploy to AWS](https://github.com/pogg144p/feedback-tickets-cloudops/actions/workflows/cd.yml/badge.svg)](https://github.com/pogg144p/feedback-tickets-cloudops/actions/workflows/cd.yml)
[![AWS Free Tier](https://img.shields.io/badge/AWS%20Cost-%240.00%2Fmonth-brightgreen)](https://aws.amazon.com/free/)
[![IaC](https://img.shields.io/badge/IaC-Terraform%20v1.8+-844FBA.svg?logo=terraform&logoColor=white)](https://terraform.io)
[![Docker](https://img.shields.io/badge/Docker-Containers%20%26%20ECR-2496ED.svg?logo=docker&logoColor=white)](https://docker.com)
[![Observability](https://img.shields.io/badge/Observability-Prometheus%20%26%20Grafana-F46800.svg?logo=grafana&logoColor=white)](https://grafana.com)

> An end-to-end, event-driven serverless data pipeline with containerized AWS Lambda microservices, automated GitHub Actions CI/CD, Terraform remote state management, and real-time Prometheus & Grafana observability — engineered strictly within the **AWS Free Tier ($0/month)**.

---

## 🏗️ Architecture & Data Flow

```
                                    ┌─────────────────────────────────────────────────────────────┐
                                    │                     AWS Cloud ($0 / month)                  │
                                    │                                                             │
  [ User / Client ]                 │  ┌──────────────┐         S3 ObjectCreated Event            │
         │                          │  │  S3 Bucket   │ ──────────────────────────────────────┐   │
         │                          │  │ (Raw Inbox)  │                                       │   │
         ▼                          │  └──────────────┘                                       ▼   │
  Upload Ticket.json ───────────────┼──────────┘                                   ┌──────────────────────┐
                                    │                                              │   Extractor Lambda   │
                                    │                                              │ (Docker via AWS ECR) │
                                    │                                              └──────────┬───────────┘
                                    │                                                         │ Async Invoke
                                    │                                                         ▼
                                    │  ┌──────────────┐                            ┌──────────────────────┐
                                    │  │   DynamoDB   │ ◄───────────────────────── │  Transformer Lambda  │
                                    │  │ (Live Table) │         Save Record        │ (Docker via AWS ECR) │
                                    │  └──────────────┘                            └──────────┬───────────┘
                                    │         ▲                                               │ Async Invoke
                                    │         │                                               ▼
                                    │  ┌──────┴───────┐                            ┌──────────────────────┐
                                    │  │  S3 Archive  │ ◄───────────────────────── │    Loader Lambda     │
                                    │  │ (Processed)  │        Archive JSON        │ (Docker via AWS ECR) │
                                    │  └──────────────┘                            └──────────┬───────────┘
                                    └─────────────────────────────────────────────────────────┼───┘
                                                                                              │
                                                                               Metric Events  │ (HTTP Push)
                                                                                              ▼
┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 Observability Stack (Docker Compose)                               │
│                                                                                                   │
│   ┌────────────────────────┐      Scrapes (5s)      ┌──────────────────┐     Queries (PromQL)     │
│   │ Prometheus Pushgateway │ ─────────────────────► │ Prometheus TSDB  │ ────────────────────┐    │
│   │      (Port 9091)       │                        │   (Port 9090)    │                     │    │
│   └────────────────────────┘                        └──────────────────┘                     ▼    │
│                                                                                     ┌──────────────────┐  │
│                                                                                     │ Grafana Dashboard│  │
│                                                                                     │   (Port 3000)    │  │
│                                                                                     └──────────────────┘  │
└───────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack & Role

| Technology | Purpose in Project |
| :--- | :--- |
| **Terraform (IaC)** | Declarative infrastructure as code managing S3 buckets, DynamoDB tables, IAM execution roles, ECR repositories, and S3 event triggers with S3 remote backend. |
| **AWS Lambda** | Event-driven microservices (`Extractor`, `Transformer`, `Loader`) executing serverless business logic in milliseconds. |
| **Docker & AWS ECR** | Containerized Lambda functions packaged using official `public.ecr.aws/lambda/python:3.12` base images with multi-layer build caching. |
| **GitHub Actions (CI/CD)**| **CI:** Flake8 linting, Pytest unit tests, `terraform fmt`, `terraform validate`.<br>**CD:** Automated Docker image build/push to ECR, and `terraform apply -auto-approve` with remote state synchronization. |
| **Prometheus & Pushgateway**| Time-series metric collection and ingestion for ephemeral serverless executions. |
| **Grafana** | Production-grade observability dashboard visualizing live ingestion rates, category breakdowns, and priority distributions. |
| **DynamoDB & S3** | NoSQL queryable database (Pay-Per-Request) and dual-bucket raw drop zone + processed audit archives. |
| **PowerShell & Bash** | Automated deployment, traffic simulation, and teardown scripts. |

---

## 📊 Live Observability Dashboard

Grafana visualizes key pipeline service-level indicators (SLIs) in real-time:
* **Total Ingestion Volume:** Real-time counter of processed feedback tickets.
* **Category Breakdown:** Donut chart dynamically classifying tickets into `Bug`, `Feature`, and `Complaint`.
* **Priority Distribution:** Color-coded severity bar graph (`High`, `Medium`, `Low`).
* **Throughput & Velocity:** Time-series pulse tracking tickets per minute.

---

## 💰 AWS Free Tier Cost Architecture

| Service | AWS Free Tier Monthly Limit | Platform Usage | Cost |
| :--- | :--- | :--- | :--- |
| **AWS Lambda** | 1,000,000 requests/month | ~1,000 requests | **$0.00** |
| **Amazon S3** | 5 GB standard storage | < 50 MB | **$0.00** |
| **Amazon DynamoDB** | 25 GB storage + 25 RCU / 25 WCU | < 10 MB | **$0.00** |
| **Amazon ECR** | 500 MB private storage/month | 3 optimized images | **$0.00** |
| **GitHub Actions** | 2,000 CI/CD build minutes/month | ~30 minutes | **$0.00** |
| **Prometheus / Grafana** | Local Docker Compose stack | Self-hosted | **$0.00** |
| **Total Monthly Spend**| — | — | **$0.00 / month** |

---

## 🚀 Quick Start Guide

### Prerequisites
* [AWS CLI v2](https://aws.amazon.com/cli/) configured with programmatic credentials.
* [Terraform v1.8+](https://www.terraform.io/downloads.html).
* [Docker Desktop](https://www.docker.com/products/docker-desktop/).

### 1. Clone Repository & Setup Infrastructure
```bash
git clone https://github.com/pogg144p/feedback-tickets-cloudops.git
cd feedback-tickets-cloudops/terraform

# Initialize Terraform with Remote S3 Backend
terraform init

# Review and apply infrastructure
terraform apply
```

### 2. Start Observability Stack
```bash
cd ../monitoring
docker compose up -d
```
Access Grafana at `http://localhost:3000` (User: `admin` / Pass: `admin`).

### 3. Simulate Live Pipeline Traffic
```powershell
# Run the automated traffic simulator (sends 10 realistic tickets)
./scripts/simulate_traffic.ps1 -Count 10
```

### 4. Clean Teardown
```powershell
./scripts/teardown.ps1
```

---

## 🧪 Automated Testing & CI/CD Pipeline

Every pull request and push to `main` triggers automated validation:
```bash
# Run unit tests locally
pytest tests/ -v

# Validate Terraform syntax
terraform fmt -check
terraform validate
```

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).
