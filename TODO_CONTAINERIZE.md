# TODO List for Containerizing Django Application for Kubernetes

- [x] Create Dockerfile for Django application (server/Dockerfile)
- [x] Create docker-compose.yml for the entire application stack (server/docker-compose.yml)
- [x] Create Kubernetes deployment YAML for MongoDB (k8s/mongodb-deployment.yaml)
- [x] Create Kubernetes deployment YAML for Node.js API (k8s/api-deployment.yaml)
- [x] Create Kubernetes deployment YAML for Django app (k8s/django-deployment.yaml)
- [x] Create Kubernetes service YAMLs for all services (k8s/services.yaml) - Services included in deployment YAMLs
- [ ] Test docker-compose locally (Docker not installed on macOS, requires Docker Desktop)
- [ ] Deploy to Kubernetes and verify (kubectl not installed, requires Kubernetes setup)
- [x] Create deployment.yaml in server directory
