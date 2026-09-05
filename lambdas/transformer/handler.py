# transformer/handler.py
# ─────────────────────────────────────────────────────────────
# LAMBDA 2 — TRANSFORMER
#
# Job: Take the raw ticket from Extractor, make sense of it.
# It reads the issue text, figures out:
#   - Category: is this a bug? a complaint? a feature request?
#   - Priority: is this high/medium/low urgency?
# Then adds a unique ticket ID + timestamps, and sends it
# to the Loader Lambda.
#
# Think of it as the "analyst" — they read the ticket and
# decide how important it is and what type it is.
# ─────────────────────────────────────────────────────────────

import json
import boto3
import os
import uuid
import logging
from datetime import datetime, timezone

logger = logging.getLogger()
logger.setLevel(logging.INFO)

lambda_client = boto3.client('lambda')

# ── Keyword Maps ──────────────────────────────────────────────
# We scan the issue text for these keywords to auto-categorize tickets.
# In a real system this might use AI/ML — but keyword matching
# is good enough to demonstrate the concept.

CATEGORY_KEYWORDS = {
    'bug': ['broken', 'error', 'not working', 'crash', 'fail', 'bug',
            'cant', "can't", 'unable', 'doesnt work', "doesn't work"],
    'complaint': ['slow', 'bad', 'terrible', 'worst', 'unhappy',
                  'disappointed', 'frustrated', 'poor', 'awful'],
    'feature': ['add', 'feature', 'would like', 'wish', 'want',
                'request', 'improve', 'enhancement', 'suggestion'],
    'question': ['how', 'what', 'when', 'where', 'why', 'help', '?', 'confused']
}

PRIORITY_KEYWORDS = {
    'high': ['urgent', 'critical', 'asap', 'immediately', 'broken',
             'cant access', "can't access", 'down', 'crash', 'emergency'],
    'medium': ['slow', 'issue', 'problem', 'not working', 'intermittent'],
    'low': ['question', 'how do i', 'wish', 'would like', 'suggestion']
}


def categorize(issue_text: str) -> str:
    """Scan issue text for keywords and return a category."""
    issue_lower = issue_text.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in issue_lower for keyword in keywords):
            return category
    return 'general'  # Default if no keywords match


def assign_priority(issue_text: str, severity: str) -> str:
    """
    Severity comes directly from the ticket (user-reported).
    We also scan the issue text to catch urgent language
    even if the user didn't mark it high severity.
    """
    # If user explicitly said high severity — trust them
    if severity == 'high':
        return 'high'

    issue_lower = issue_text.lower()
    for priority, keywords in PRIORITY_KEYWORDS.items():
        if any(keyword in issue_lower for keyword in keywords):
            return priority

    return 'low'  # Default priority


def handler(event, context):
    """
    'event' here is NOT an S3 trigger — it's the raw ticket data
    sent directly from the Extractor Lambda as a JSON payload.
    """
    raw_ticket = event

    issue_text = raw_ticket.get('issue', '')
    severity = raw_ticket.get('severity', 'low')

    # ── Generate unique ticket ID ─────────────────────────────
    # Format: TKT-20260825-A3F9B2C1
    # Date prefix makes it easy to sort/search by date
    date_str = datetime.now(timezone.utc).strftime('%Y%m%d')
    unique_suffix = str(uuid.uuid4())[:8].upper()
    ticket_id = f"TKT-{date_str}-{unique_suffix}"

    now = datetime.now(timezone.utc).isoformat()

    # ── Build the processed ticket record ─────────────────────
    processed_ticket = {
        'ticket_id':    ticket_id,
        'user':         raw_ticket.get('user', 'unknown'),
        'email':        raw_ticket.get('email', ''),
        'issue':        issue_text,
        'severity':     severity,
        'category':     categorize(issue_text),
        'priority':     assign_priority(issue_text, severity),
        'status':       'processed',
        'source_key':   raw_ticket.get('source_key', ''),
        'created_at':   now,
        'processed_at': now
    }

    logger.info(
        f"Ticket {ticket_id} processed | "
        f"Category: {processed_ticket['category']} | "
        f"Priority: {processed_ticket['priority']}"
    )

    # ── Send to Loader Lambda ─────────────────────────────────
    loader_name = os.environ['LOADER_FUNCTION_NAME']

    lambda_client.invoke(
        FunctionName=loader_name,
        InvocationType='Event',
        Payload=json.dumps(processed_ticket)
    )

    logger.info(f"Ticket {ticket_id} handed off to Loader")

    return {
        'statusCode': 200,
        'body': f"Ticket {ticket_id} transformed successfully"
    }
