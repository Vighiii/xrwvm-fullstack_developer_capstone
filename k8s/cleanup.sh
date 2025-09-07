#!/bin/bash

# Cleanup Kubernetes resources
echo "🧹 Cleaning up Kubernetes resources..."

kubectl delete -f k8s/django-service.yaml
kubectl delete -f k8s/api-service.yaml
kubectl delete -f k8s/mongodb.yaml
kubectl delete -f k8s/configmap.yaml

echo "✅ Kubernetes resources cleaned up!"
