# Kubernetes Container Orchestration (EKS / Minikube)

This directory provides declarative Kubernetes manifests to deploy, scale, and manage the Feedback Tickets microservice workloads on a Kubernetes cluster (such as **Amazon EKS**, **Minikube**, or **Docker Desktop Kubernetes**).

---

## 🏗️ Architecture & Resources

```
k8s/
├── namespace.yaml      # Dedicated 'tickets-cloudops' isolation boundary
├── configmap.yaml      # Non-confidential runtime configuration
├── secret.yaml         # Opaque credentials & tokens (encrypted in etcd)
├── deployment.yaml     # 3 Replicas, rolling zero-downtime updates, liveness/readiness probes
├── service.yaml        # LoadBalancer service exposing TCP port 80 -> 8080
├── hpa.yaml            # Horizontal Pod Autoscaler (2-10 pods, CPU > 70% threshold)
├── ingress.yaml        # NGINX Ingress rules & TLS termination
└── README.md           # Architecture & Interview guide
```

---

## 🚀 Deployment Guide (Local / EKS)

### Option A: Testing Locally with Minikube / Docker Desktop
Ensure Kubernetes is enabled in Docker Desktop settings or run:

```bash
minikube start --driver=docker
```

### Apply all manifests in order:
```bash
# 1. Create namespace
kubectl apply -f k8s/namespace.yaml

# 2. Deploy configs and secrets
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml

# 3. Deploy workload and networking
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml
kubectl apply -f k8s/ingress.yaml
```

### Inspect running cluster resources:
```bash
kubectl get all -n tickets-cloudops
kubectl describe deployment tickets-app-deployment -n tickets-cloudops
```

---

## 💼 DevOps & Cloud Resume Bullets & Interview Talking Points

### Resume Bullet Point:
> *"Architected and deployed production Kubernetes manifests (Deployments, Services, ConfigMaps, Secrets, Ingress, HPA) for containerized microservices; implemented zero-downtime rolling updates (`maxSurge=1`, `maxUnavailable=0`), automated self-healing via liveness/readiness probes, and horizontal pod autoscaling based on CPU utilization."*

### Key Concepts to Explain in Interviews:
- **Zero-Downtime Deployments:** Configured `RollingUpdate` with `maxUnavailable: 0` ensuring at least 100% of desired pods are continuously healthy while new replica revisions spin up.
- **Self-Healing Infrastructure:** Configured distinct `livenessProbe` (detects deadlock / memory leaks and restarts container) and `readinessProbe` (stops sending ingress traffic until database/S3 connections initialize).
- **Resource Quotas & Limits:** Enforced explicit container `requests` and `limits` to prevent CPU starvation and OOMKilled errors across the Kubernetes node worker pool.
- **HPA Flapping Prevention:** Added stabilization windows (`scaleDown.stabilizationWindowSeconds: 300`) to prevent rapid pod thrashing during short traffic bursts.
