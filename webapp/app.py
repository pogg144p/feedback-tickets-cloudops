"""
app.py
─────────────────────────────────────────────────────────────
Public Feedback Tickets Web Portal
Deployable to Render (Free Tier) / Docker / Local
─────────────────────────────────────────────────────────────
Provides:
  1. GET  /         : Interactive ticket submission portal
  2. POST /submit   : Ingests ticket directly into S3 Raw Bucket
  3. GET  /tickets  : Live operational dashboard querying DynamoDB
  4. GET  /healthz  : Service health check endpoint
─────────────────────────────────────────────────────────────
"""

import os
import json
import uuid
import logging
from datetime import datetime, timezone
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import boto3
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "cloudops-dev-secret-key-3482")

# Environment configurations
AWS_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
RAW_BUCKET_NAME = os.environ.get("S3_RAW_BUCKET", "feedback-tickets-raw-dev-768229077155")
DYNAMODB_TABLE_NAME = os.environ.get("DYNAMODB_TABLE", "feedback-tickets-table-dev")

# Initialize AWS clients
s3_client = boto3.client("s3", region_name=AWS_REGION)
dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
tickets_table = dynamodb.Table(DYNAMODB_TABLE_NAME)


@app.route("/")
def index():
    """Renders the ticket submission portal."""
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit_ticket():
    """
    Submits a ticket into the raw S3 ingestion bucket,
    which automatically triggers the serverless ETL pipeline.
    """
    customer_id = request.form.get("customer_id", "").strip() or f"cust-{uuid.uuid4().hex[:4]}"
    subject = request.form.get("subject", "").strip()
    description = request.form.get("description", "").strip()

    if not subject or not description:
        flash("Subject and description cannot be empty!", "error")
        return redirect(url_for("index"))

    ticket_payload = {
        "customer_id": customer_id,
        "subject": subject,
        "description": description,
        "submitted_at": datetime.now(timezone.utc).isoformat()
    }

    object_key = f"incoming/{uuid.uuid4().hex}.json"

    try:
        s3_client.put_object(
            Bucket=RAW_BUCKET_NAME,
            Key=object_key,
            Body=json.dumps(ticket_payload, indent=2),
            ContentType="application/json"
        )
        logger.info(f"Successfully uploaded ticket to s3://{RAW_BUCKET_NAME}/{object_key}")
        flash(f"Ticket submitted successfully! Ingested into S3 landing bucket. Pipeline is processing in the background.", "success")
        return redirect(url_for("live_tickets", processing="1"))
    except ClientError as e:
        logger.error(f"S3 upload error: {e}")
        flash(f"Failed to submit ticket: {e.response['Error']['Message']}", "error")
        return redirect(url_for("index"))


@app.route("/tickets")
def live_tickets():
    """
    Scans the DynamoDB table and renders the live feed of processed tickets.
    """
    try:
        response = tickets_table.scan(Limit=50)
        items = response.get("Items", [])
        # Sort items by processed_at descending
        items.sort(key=lambda x: x.get("processed_at", ""), reverse=True)

        stats = {
            "total": len(items),
            "bugs": sum(1 for i in items if i.get("category") == "bug"),
            "features": sum(1 for i in items if i.get("category") == "feature_request"),
            "billing": sum(1 for i in items if i.get("category") == "billing"),
            "high_priority": sum(1 for i in items if i.get("priority") == "high"),
        }
    except Exception as e:
        logger.error(f"DynamoDB scan error: {e}")
        items = []
        stats = {"total": 0, "bugs": 0, "features": 0, "billing": 0, "high_priority": 0}
        flash(f"Unable to load tickets from DynamoDB: {str(e)}", "error")

    is_processing = request.args.get("processing") == "1"
    return render_template("tickets.html", tickets=items, stats=stats, is_processing=is_processing)


@app.route("/api/tickets")
def api_tickets():
    """API endpoint returning live tickets as JSON."""
    try:
        response = tickets_table.scan(Limit=50)
        items = response.get("Items", [])
        return jsonify({"status": "success", "count": len(items), "tickets": items})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/healthz")
def healthz():
    """Health check endpoint for Render / Kubernetes."""
    return jsonify({"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat()}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
