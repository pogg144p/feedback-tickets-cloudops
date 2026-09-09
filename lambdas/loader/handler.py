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
import urllib.request
import urllib.parse
from datetime import datetime, timezone

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# AWS clients
dynamodb = boto3.resource('dynamodb')
s3_client = boto3.client('s3')
sns_client = boto3.client('sns')


def send_alerts(ticket):
    """
    Sends multi-channel alerts for critical bugs:
      1. AWS SNS Topic (fans out to Email + SQS Queue)
      2. Telegram Bot (instant mobile push notification)
    """
    ticket_id = ticket.get('ticket_id')
    subject = ticket.get('subject', 'No Subject')
    description = ticket.get('description', 'No Description')
    category = ticket.get('category')
    priority = ticket.get('priority')

    alert_message = (
        f"🚨 CRITICAL BUG DETECTED\n"
        f"────────────────────────────\n"
        f"Ticket ID : {ticket_id}\n"
        f"Category  : {category.upper()}\n"
        f"Priority  : {priority.upper()}\n"
        f"Subject   : {subject}\n"
        f"Details   : {description}\n"
        f"Time      : {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}"
    )

    # ── 1. Publish to SNS Topic (Email + SQS Queue) ───────────
    sns_topic_arn = os.environ.get('SNS_TOPIC_ARN')
    if sns_topic_arn:
        try:
            sns_client.publish(
                TopicArn=sns_topic_arn,
                Subject=f"🚨 [CRITICAL BUG] {ticket_id}: {subject[:50]}",
                Message=alert_message
            )
            logger.info(f"Published critical alert to SNS: {sns_topic_arn}")
        except Exception as e:
            logger.error(f"Failed to publish to SNS: {str(e)}")

    # ── 2. Send Telegram Bot Push Notification ────────────────
    telegram_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    telegram_chat_id = os.environ.get('TELEGRAM_CHAT_ID')

    if telegram_token and telegram_chat_id:
        try:
            url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
            payload = json.dumps({
                "chat_id": telegram_chat_id,
                "text": alert_message,
                "parse_mode": "Markdown"
            }).encode('utf-8')

            req = urllib.request.Request(
                url,
                data=payload,
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    logger.info("Critical bug alert sent to Telegram successfully.")
        except Exception as e:
            logger.error(f"Failed to send Telegram alert: {str(e)}")


def handler(event, context):
    """
    'event' is the fully processed ticket JSON sent from Transformer.
    We save it to DynamoDB, archive it to S3, and trigger alerts if critical.
    """
    processed_ticket = event
    ticket_id = processed_ticket['ticket_id']

    # ── Step 1: Write to DynamoDB ─────────────────────────────
    table_name = os.environ['DYNAMODB_TABLE_NAME']
    table = dynamodb.Table(table_name)
    table.put_item(Item=processed_ticket)
    logger.info(f"Ticket {ticket_id} saved to DynamoDB table: {table_name}")

    # ── Step 2: Archive to S3 Processed Bucket ───────────────
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

    # ── Step 3: Trigger Multi-Channel Alert if Critical Bug ───
    if processed_ticket.get('category') == 'bug' and processed_ticket.get('priority') == 'high':
        logger.info(f"Ticket {ticket_id} is a CRITICAL BUG! Dispatching alerts...")
        send_alerts(processed_ticket)

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
