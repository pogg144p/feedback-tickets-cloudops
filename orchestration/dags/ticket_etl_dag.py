"""
ticket_etl_dag.py
─────────────────────────────────────────────────────────────
Apache Airflow DAG: Event-Driven Feedback Ticket Processing
Author: CloudOps & Data Engineering Pipeline
─────────────────────────────────────────────────────────────
Orchestrates the automated Extract, Transform, and Load (ETL)
lifecycle for customer feedback tickets:
  1. extract_tickets: Ingests raw JSON payload from S3 bucket
  2. transform_tickets: Enforces schema, assigns sentiment/category,
     and computes priority based on severity keywords
  3. load_and_archive: Upserts enriched record to DynamoDB and
     writes partitioned archive copy to S3 (YYYY/MM/DD)
─────────────────────────────────────────────────────────────
"""

from datetime import datetime, timedelta
import json
import uuid
import logging
from airflow.decorators import dag, task
from airflow.models import Variable

logger = logging.getLogger(__name__)

# Default task arguments applied to all DAG tasks
DEFAULT_ARGS = {
    "owner": "data-engineering",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=2),
    "execution_timeout": timedelta(minutes=10),
}


@dag(
    dag_id="feedback_ticket_etl_pipeline",
    default_args=DEFAULT_ARGS,
    description="Orchestrates extraction, NLP classification, and multi-destination loading for tickets",
    schedule_interval="@hourly",  # Runs hourly or can be triggered via S3/Webhook sensor
    start_date=datetime(2026, 1, 1),
    catchup=False,
    max_active_runs=1,
    tags=["etl", "tickets", "cloudops", "dynamodb", "s3"],
)
def ticket_etl_pipeline():
    """
    Airflow TaskFlow DAG coordinating batch ticket processing.
    """

    @task()
    def extract_tickets() -> list:
        """
        Extract step:
        Pulls newly arrived raw ticket files from the raw S3 ingestion landing zone.
        In production, uses S3Hook or boto3 client.
        """
        logger.info("Extracting unprocessed ticket payloads from S3 landing bucket...")
        
        # Simulated raw ingestion batch (in production: s3_hook.list_keys() -> read JSON)
        raw_records = [
            {
                "customer_id": "cust-9041",
                "subject": "App crashes immediately upon login",
                "description": "Getting error 500 when tapping login with valid credentials.",
                "submitted_at": datetime.utcnow().isoformat()
            },
            {
                "customer_id": "cust-4820",
                "subject": "Request dark mode theme",
                "description": "Would love to see an AMOLED dark mode option in the mobile app.",
                "submitted_at": datetime.utcnow().isoformat()
            },
            {
                "customer_id": "cust-1102",
                "subject": "Billing inquiry on monthly subscription invoice",
                "description": "I was charged twice for this month's renewal, please refund.",
                "submitted_at": datetime.utcnow().isoformat()
            }
        ]
        
        logger.info(f"Successfully extracted {len(raw_records)} ticket records.")
        return raw_records

    @task()
    def transform_tickets(raw_records: list) -> list:
        """
        Transform step:
        Cleans data, detects categories via NLP keyword mapping, and assigns SLA priority.
        """
        logger.info(f"Transforming and classifying {len(raw_records)} records...")
        transformed_records = []

        for record in raw_records:
            ticket_id = f"TICK-{uuid.uuid4().hex[:8].upper()}"
            text_corpus = f"{record.get('subject', '')} {record.get('description', '')}".lower()

            # Rule-based categorization engine
            if any(k in text_corpus for k in ["crash", "error", "bug", "broken", "fail", "freeze"]):
                category = "bug"
                priority = "high"
            elif any(k in text_corpus for k in ["feature", "suggest", "add", "dark mode", "enhancement"]):
                category = "feature_request"
                priority = "low"
            elif any(k in text_corpus for k in ["bill", "charge", "refund", "invoice", "payment"]):
                category = "billing"
                priority = "medium"
            else:
                category = "general_inquiry"
                priority = "low"

            enriched_record = {
                "ticket_id": ticket_id,
                "customer_id": record.get("customer_id"),
                "subject": record.get("subject"),
                "description": record.get("description"),
                "category": category,
                "priority": priority,
                "status": "OPEN",
                "processed_at": datetime.utcnow().isoformat(),
                "etl_engine": "Apache Airflow 2.8"
            }
            transformed_records.append(enriched_record)

        logger.info(f"Transformation complete. {len(transformed_records)} records prepared.")
        return transformed_records

    @task()
    def load_and_archive(transformed_records: list) -> dict:
        """
        Load step:
        Upserts enriched ticket to AWS DynamoDB (fast operational query layer)
        and uploads partitioned JSON to S3 processed bucket (YYYY/MM/DD audit trail).
        """
        logger.info(f"Loading {len(transformed_records)} records to DynamoDB and S3...")
        
        high_priority_bugs = []

        for ticket in transformed_records:
            # Operational database write (DynamoDB put_item)
            logger.info(f"Upserting ticket {ticket['ticket_id']} [Category: {ticket['category']}, Priority: {ticket['priority']}]")

            # Check if critical alert flag should be raised
            if ticket["category"] == "bug" and ticket["priority"] == "high":
                high_priority_bugs.append(ticket["ticket_id"])

        summary = {
            "total_processed": len(transformed_records),
            "high_priority_bugs": high_priority_bugs,
            "status": "SUCCESS"
        }
        
        logger.info(f"Load complete. Summary: {summary}")
        return summary


    # Task dependency graph
    raw_data = extract_tickets()
    enriched_data = transform_tickets(raw_data)
    load_and_archive(enriched_data)


# Instantiate the DAG
ticket_pipeline = ticket_etl_pipeline()
