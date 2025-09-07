#!/bin/bash

# Build Docker images for Kubernetes deployment
echo "🏗️  Building Docker images for Kubernetes..."

# Build API service image
echo "Building API service image..."
docker build -t dealership-api:latest ./server/database/

# Build Django service image
echo "Building Django service image..."
docker build -t dealership-django:latest ./server/

echo "✅ Docker images built successfully!"

# Apply Kubernetes configurations
echo "🚀 Deploying to Kubernetes..."

# Apply configurations in order
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/mongodb.yaml
kubectl apply -f k8s/api-service.yaml
kubectl apply -f k8s/django-service.yaml

echo "⏳ Waiting for deployments to be ready..."

# Wait for deployments
kubectl wait --for=condition=available --timeout=300s deployment/mongodb
kubectl wait --for=condition=available --timeout=300s deployment/dealership-api
kubectl wait --for=condition=available --timeout=300s deployment/dealership-django

echo "✅ Kubernetes deployment complete!"

# Show status
echo "📊 Deployment Status:"
kubectl get pods
echo ""
kubectl get services

echo ""
echo "🌐 Access your application:"
echo "Django App: kubectl port-forward service/dealership-django-service 8000:8000"
echo "API Service: kubectl port-forward service/dealership-api-service 3030:3030"
