# Kubernetes Deployment for Dealership Management System

This directory contains Kubernetes deployment files for the Dealership Management System.

## Quick Deploy to Kubernetes

```bash
# Apply all configurations
kubectl apply -f k8s/

# Check deployment status
kubectl get pods
kubectl get services

# Access the application
kubectl port-forward service/dealership-django-service 8000:8000
```

## Components

- **MongoDB**: Database with persistent storage
- **API Service**: Node.js/Express API
- **Django Service**: Main application server
- **ConfigMap**: Environment configuration
- **Persistent Volume**: Database storage

## Services

- Django App: http://localhost:8000
- API Service: http://localhost:3030
- MongoDB: Internal cluster communication

## Scaling

```bash
# Scale Django service
kubectl scale deployment dealership-django --replicas=3

# Scale API service
kubectl scale deployment dealership-api --replicas=2
```

## Monitoring

```bash
# View logs
kubectl logs -f deployment/dealership-django
kubectl logs -f deployment/dealership-api
kubectl logs -f deployment/mongodb

# Check resource usage
kubectl top pods
```
