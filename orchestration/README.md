# Apache Airflow Data Pipeline Orchestration

This module provides batch and micro-batch workflow orchestration for the Feedback Tickets processing pipeline, implemented using **Apache Airflow 2.8+ TaskFlow API**.

---

## 🎯 Purpose & Data Architecture

While AWS Lambda provides event-driven, real-time ingestion, **Apache Airflow** provides robust enterprise orchestration capabilities:
- **Directed Acyclic Graphs (DAGs):** Clear visual dependency management between extraction, transformation, and multi-sink loading.
- **Automated Retries & Backoff:** Built-in resilience (`retries=3`, `retry_delay=2m`) against intermittent database connection drops or API rate limits.
- **Backfill & Historical Re-runs:** Seamlessly re-execute past data partitions without duplicating records.
- **Monitoring & SLAs:** Built-in execution timeout handling, alerting hooks, and task status logs.

---

## 📂 Workflow Architecture

```
                       [extract_tickets]
               (Extract raw ticket batch from S3)
                               │
                               ▼
                     [transform_tickets]
             (NLP Classification & SLA Priority Logic)
                               │
                               ▼
                     [load_and_archive]
          ┌────────────────────┴────────────────────┐
          ▼                                         ▼
   DynamoDB Table                              S3 Bucket
 (Operational Lookups)                  (YYYY/MM/DD Partitions)
```

---

## 🚀 Running Airflow Locally

To spin up the local Airflow Web UI and test DAG runs:

```bash
cd orchestration
docker compose -f docker-compose.airflow.yml up -d
```

1. Navigate to: `http://localhost:8080`
2. Login with:
   - **Username:** `admin`
   - **Password:** `admin`
3. Locate DAG: `feedback_ticket_etl_pipeline` and trigger a manual test run.

---

## 💼 Data Engineering Resume Bullets & Interview Talking Points

### Resume Bullet Point:
> *"Orchestrated high-reliability batch data pipelines using Apache Airflow (TaskFlow API); automated ticket extraction from S3, rule-based NLP classification, and concurrent loading into DynamoDB and date-partitioned S3 storage with automated retry policies."*

### Key Concepts to Mention in Interviews:
- **TaskFlow API vs Classic Operators:** Built using modern Python decorators (`@dag`, `@task`), passing data cleanly between tasks using Airflow XComs automatically.
- **Idempotency & Partitioning:** Data loading to S3 follows structured date-partitioning (`processed/YYYY/MM/DD/`), allowing idempotent backfills without corrupted duplicate keys.
- **Error Recovery:** Configured exponential backoffs and dead-letter detection for high-priority bug tickets requiring immediate intervention.
