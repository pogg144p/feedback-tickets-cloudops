# Observability & Incident Response (Prometheus, Alertmanager, Grafana)

This directory contains the production monitoring, dashboarding, and automated alerting stack for the Serverless CloudOps Feedback Tickets Pipeline.

---

## 🏛️ Observability Architecture

```
                                  AWS Lambdas
                               (Batch & Stream)
                                      │
                                      ▼
                            Prometheus Pushgateway
                                  (Port 9091)
                                      │  (scraped every 5s)
                                      ▼
                                 Prometheus
                                  (Port 9090)
                         ┌────────────┴────────────┐
                         ▼                         ▼
                  Alertmanager                  Grafana
                   (Port 9093)                (Port 3000)
                         │                         │
             ┌───────────┴───────────┐      [Visual Dashboards]
             ▼                       ▼      - Ticket Volume
       Incident Webhooks        Email/Pager - Category Donut
       (Spike Detection)        (Target Down) - Latency Quantiles
```

---

## 🚨 Alert Rules Configured (`alerts.yml`)

1. **`CriticalBugSpikeDetected`** (Severity: `critical`): Fires if high-priority bug ingestion exceeds `0.5 tickets/sec` over 5 minutes.
2. **`PipelineProcessingFailureRateHigh`** (Severity: `warning`): Triggers if processing errors in Lambda exceed `0.1 errors/sec` over 2 minutes.
3. **`TicketProcessingLatencyHigh`** (Severity: `warning`): Evaluates p95 processing duration (`histogram_quantile`) and alerts if processing exceeds 5 seconds.
4. **`MonitoringTargetUnreachable`** (Severity: `page`): Instantly triggers a page if Pushgateway or scrapers fail health checks for > 1 minute.

---

## 🛠️ Running the Full Monitoring Stack

```bash
cd monitoring
docker compose up -d
```

### Endpoints:
- **Grafana Dashboard:** `http://localhost:3000` (admin/admin)
- **Prometheus UI & Rules:** `http://localhost:9090/alerts`
- **Alertmanager UI & Silences:** `http://localhost:9093`
- **Pushgateway Metrics:** `http://localhost:9091`

---

## 💼 DevOps & SRE Resume Bullets & Interview Talking Points

### Resume Bullet Point:
> *"Implemented real-time production alerting using Prometheus PromQL rules and Alertmanager; configured automated deduplication, latency degradation alerts (p95 SLA thresholds), and alert inhibition to minimize alert fatigue."*

### Key Concepts to Mention in Interviews:
- **Alert Fatigue & Inhibition:** Configured `inhibit_rules` so low-priority warning notifications are suppressed if a critical alert is already active for the same application tier.
- **SLIs & SLOs:** Monitored error budgets using `rate(tickets_processing_errors_total)` and p95 latency quantiles rather than noisy instantaneous CPU/memory spikes.
- **Pushgateway Pattern:** Lambdas are ephemeral and cannot be scraped by Prometheus. We used Pushgateway as an intermediary buffer so short-lived serverless tasks can report custom metrics.
