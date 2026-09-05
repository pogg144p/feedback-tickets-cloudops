# loader/handler.py
# ─────────────────────────────────────────────────────────────
# LAMBDA 3 — LOADER
#
# Job: Take the fully processed ticket from Transformer and
# save it in TWO places:
#   1. DynamoDB → the live database (queryable, fast lookups)
#   2. S3 processed bucket → permanent archive (for audit/backup)
#
# Think of it as the "filing clerk" — they take the completed
# paperwork and put it in the right cabinet AND make a photocopy
# for the archive room.
# ─────────────────────────────────────────────────────────────

import json
import boto3
import os
import logging
from datetime import datetime, timezone

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# DynamoDB resource (higher-level API than client — easier for put/get/query)
dynamodb = boto3.resource('dynamodb')
s3_client = boto3.client('s3')


def handler(event, context):
    """
    'event' is the fully processed ticket JSON sent from Transformer.
    We save it to DynamoDB and archive it to S3.
    """
    processed_ticket = event
    ticket_id = processed_ticket['ticket_id']

    # ── Step 1: Write to DynamoDB ─────────────────────────────
    # put_item() = insert or replace a record (upsert)
    # The table name comes from an environment variable set by Terraform
    table_name = os.environ['DYNAMODB_TABLE_NAME']
    table = dynamodb.Table(table_name)

    table.put_item(Item=processed_ticket)
    logger.info(f"Ticket {ticket_id} saved to DynamoDB table: {table_name}")

    # ── Step 2: Archive to S3 Processed Bucket ───────────────
    # We organize archived tickets by date: processed/YYYY/MM/DD/ticket_id.json
    # This makes it easy to find all tickets from a specific day later.
    processed_bucket = os.environ['PROCESSED_BUCKET_NAME']
    now = datetime.now(timezone.utc)
    s3_key = f"processed/{now.strftime('%Y/%m/%d')}/{ticket_id}.json"

    s3_client.put_object(
        Bucket=processed_bucket,
        Key=s3_key,
        Body=json.dumps(processed_ticket, indent=2),
        ContentType='application/json'
    )
    logger.info(f"Ticket {ticket_id} archived to s3://{processed_bucket}/{s3_key}")

    # ── Done ──────────────────────────────────────────────────
    logger.info(f"Pipeline complete for ticket {ticket_id}")

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': f"Ticket {ticket_id} loaded successfully",
            'dynamodb_table': table_name,
            'archive_path': f"s3://{processed_bucket}/{s3_key}"
        })
    }
