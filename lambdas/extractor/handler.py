# extractor/handler.py
# ─────────────────────────────────────────────────────────────
# LAMBDA 1 — EXTRACTOR
#
# Job: Watch the raw S3 bucket. The moment a ticket JSON file
# lands there, this Lambda wakes up automatically (S3 triggers it).
# It reads the file, checks it's valid, then passes it to the
# Transformer Lambda.
#
# Think of it as the "receptionist" — it receives the ticket,
# checks it's not garbage, then hands it to the right team.
# ─────────────────────────────────────────────────────────────

import json
import boto3
import os
import logging

# Set up logging — you'll see these messages in AWS Lambda logs
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# boto3 is the Python SDK for AWS — how Python talks to AWS services
s3_client = boto3.client('s3')
lambda_client = boto3.client('lambda')


def handler(event, context):
    """
    'event'   → AWS automatically fills this with info about what triggered us.
                When S3 triggers Lambda, event contains the bucket name + file key.
    'context' → Runtime info (how much memory, time remaining, etc.) — we won't use it much.
    """

    # ── Step 1: Find out which file was just uploaded ─────────
    # When S3 triggers Lambda, it sends a "Records" list.
    # We grab the first record (we process one file at a time).
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']

    logger.info(f"New ticket file detected: s3://{bucket_name}/{file_key}")

    # ── Step 2: Read the JSON file from S3 ───────────────────
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        raw_content = response['Body'].read().decode('utf-8')
        ticket_data = json.loads(raw_content)
    except json.JSONDecodeError:
        logger.error(f"File {file_key} is not valid JSON. Skipping.")
        return {'statusCode': 400, 'body': 'Invalid JSON file'}
    except Exception as e:
        logger.error(f"Failed to read file from S3: {str(e)}")
        raise

    # ── Step 3: Validate required fields ─────────────────────
    # Every ticket MUST have these 3 fields. Reject if missing.
    required_fields = ['user', 'email', 'issue']
    for field in required_fields:
        if field not in ticket_data:
            logger.error(f"Ticket rejected — missing required field: '{field}'")
            return {'statusCode': 400, 'body': f"Missing field: {field}"}

    logger.info(f"Ticket from '{ticket_data['user']}' validated successfully")

    # ── Step 4: Add source info and pass to Transformer ──────
    # We attach where this ticket came from (which file in S3)
    # so Loader can archive it properly later.
    ticket_data['source_bucket'] = bucket_name
    ticket_data['source_key'] = file_key

    # Invoke the Transformer Lambda asynchronously
    # InvocationType='Event' = fire and forget (async) — we don't wait for response
    transformer_name = os.environ['TRANSFORMER_FUNCTION_NAME']

    lambda_client.invoke(
        FunctionName=transformer_name,
        InvocationType='Event',
        Payload=json.dumps(ticket_data)
    )

    logger.info(f"Ticket handed off to Transformer: {transformer_name}")

    return {
        'statusCode': 200,
        'body': f"Ticket from {ticket_data['user']} extracted and forwarded"
    }
