# BlackFalcon Deployment Guide

This guide covers deploying BlackFalcon using Docker Compose and Kubernetes.

## Prerequisites
- Docker & Docker Compose
- Kubernetes cluster (for K8s deployment)

## 1. Local / Standalone Deployment (Docker Compose)

The easiest way to run BlackFalcon in production is via `docker-compose`.

```bash
# Build and start the containers in detached mode
docker-compose up -d --build

# View logs
docker-compose logs -f
```

The application will be available at:
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`

## 2. Enterprise Deployment (Kubernetes)

For highly available, scalable deployments, apply the manifests in the `k8s/` directory.

```bash
# Apply ConfigMaps and Secrets first
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secrets.yaml

# Apply the Backend Deployment and Service
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/backend-service.yaml

# Apply the Frontend Deployment and Service
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/frontend-service.yaml
```

## Security Best Practices
- **Secrets**: Do not commit `secrets.yaml` to source control. Use a secret manager like HashiCorp Vault or AWS Secrets Manager.
- **TLS/SSL**: Terminate SSL at the Ingress controller or Load Balancer level.
- **Database**: In production, do not use SQLite. Configure the backend to use an external PostgreSQL cluster via the `DATABASE_URL` environment variable.
