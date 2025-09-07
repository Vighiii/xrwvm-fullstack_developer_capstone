# 🚗 Dealership Management System - Bulletproof Deployment

> **A complete full-stack dealership management application with bulletproof containerized deployment**

![Deployment Status](https://img.shields.io/badge/deployment-bulletproof-green)
![Docker](https://img.shields.io/badge/docker-ready-blue)
![Health Checks](https://img.shields.io/badge/health%20checks-automated-brightgreen)

## 🌟 Features

- **Full-Stack Application**: Django web app with Node.js API and MongoDB
- **Bulletproof Deployment**: Automated containerization with health monitoring
- **Comprehensive Health Checks**: Service validation and automated recovery
- **Production Ready**: Optimized builds with dependency management
- **Developer Friendly**: Quick start scripts and detailed monitoring

## 🚀 Quick Start

### Prerequisites
- Docker Desktop installed and running
- Git (for cloning)

### One-Command Deployment

```bash
# Clone and deploy in one go
git clone https://github.com/emiflair/xrwvm-fullstack_developer_capstone.git
cd xrwvm-fullstack_developer_capstone
git checkout containerize-k8s
./quick-deploy.sh
```

That's it! Your application will be running at:
- **Main App**: http://localhost:8000
- **API Service**: http://localhost:3030  
- **MongoDB**: mongodb://localhost:27017

## 📚 Deployment Scripts

### 🎯 `quick-deploy.sh` - Complete Deployment
Full deployment automation with health checks and recovery:
```bash
./quick-deploy.sh
```
**Features:**
- Prerequisites checking
- Container cleanup
- Service health monitoring
- Automated recovery on failures
- Comprehensive validation

### ⚡ `simple-start.sh` - Quick Development Start
Fast startup for development:
```bash
./simple-start.sh
```

### 🏥 `health-check.sh` - Service Monitoring
Check all services health status:
```bash
./health-check.sh
```

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Django Web    │    │   Node.js API   │    │    MongoDB      │
│   (Port 8000)   │◄──►│   (Port 3030)   │◄──►│   (Port 27017)  │
│                 │    │                 │    │                 │
│ • Web Interface │    │ • REST API      │    │ • Data Storage  │
│ • Authentication│    │ • CRUD Ops      │    │ • Persistence   │
│ • Static Files  │    │ • JSON Responses│    │ • Replication   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🛠️ Services Overview

### Django Web Application
- **Framework**: Django 4.2.24
- **Purpose**: Main web interface and user management
- **Features**: Authentication, dealership management, review system
- **Health Check**: `http://localhost:8000/health/`

### Node.js API Service
- **Framework**: Express.js
- **Purpose**: RESTful API for data operations
- **Features**: CRUD operations, JSON responses, MongoDB integration
- **Health Check**: `http://localhost:3030/health`

### MongoDB Database
- **Version**: MongoDB 6.0
- **Purpose**: Data persistence and storage
- **Features**: Document storage, indexing, replication ready
- **Credentials**: admin/password (development)

## 🔧 Development Commands

```bash
# View all service logs
docker-compose logs -f

# Check service status
docker-compose ps

# Restart specific service
docker-compose restart dealership_django

# Stop all services
docker-compose down

# Rebuild and restart
docker-compose up --build -d

# Access MongoDB shell
docker exec -it dealership_mongodb mongosh

# Access Django shell
docker exec -it dealership_django python manage.py shell
```

## 📊 Monitoring & Health Checks

The deployment system includes comprehensive health monitoring:

### Automated Health Checks
- **Container Health**: Docker health checks for all services
- **Service Endpoints**: HTTP endpoint validation
- **Database Connectivity**: MongoDB connection testing
- **Dependency Management**: Service startup ordering

### Health Check Endpoints
- Django: `GET /health/`
- API: `GET /health`
- MongoDB: Shell ping command

### Recovery Mechanisms
- Automatic service restart on failure
- Container dependency management
- Health check retries with exponential backoff
- Graceful degradation on partial failures

## 🐳 Docker Configuration

### Services
- **MongoDB**: mongo:6.0 with persistent volumes
- **API**: Custom Node.js image with health checks
- **Django**: Custom Django image with static file management

### Volumes
- `mongodb_data`: Persistent database storage
- `mongodb_config`: Database configuration
- Static files and media volumes

### Networks
- `dealership_network`: Isolated container network

## 🔒 Security Features

- **Container Isolation**: Each service runs in isolated containers
- **Network Security**: Services communicate over internal Docker network
- **Environment Variables**: Sensitive data managed via environment
- **Volume Mounting**: Secure data persistence
- **Health Monitoring**: Continuous service validation

## 🚨 Troubleshooting

### Common Issues

**Services not starting:**
```bash
# Check container status
docker-compose ps

# View detailed logs
docker-compose logs -f [service_name]

# Restart problematic service
docker-compose restart [service_name]
```

**Port conflicts:**
```bash
# Check what's using the ports
lsof -i :8000
lsof -i :3030
lsof -i :27017

# Stop conflicting services or change ports in docker-compose.yml
```

**Database connection issues:**
```bash
# Check MongoDB container
docker exec dealership_mongodb mongosh --eval "db.adminCommand('ping')"

# Check API connectivity
curl http://localhost:3030/health
```

### Log Locations
- Deployment logs: `deployment.log`
- Container logs: `docker-compose logs [service]`
- Application logs: Available via container exec

## 📈 Performance Optimization

### Build Optimization
- `.dockerignore` files for clean builds
- Multi-stage Docker builds where applicable
- Dependency caching optimization
- Static file serving optimization

### Runtime Optimization
- Health check intervals optimized for quick detection
- Container resource limits configured
- Network optimization for inter-service communication
- Volume mounting for persistent data

## 🔄 CI/CD Ready

The bulletproof deployment system is designed for:
- **Continuous Integration**: Automated testing and validation
- **Continuous Deployment**: One-command deployment process
- **Environment Parity**: Development/production consistency
- **Scalability**: Ready for orchestration platforms

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Test with: `./health-check.sh`
5. Commit: `git commit -m 'Add amazing feature'`
6. Push: `git push origin feature/amazing-feature`
7. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with Django, Node.js, and MongoDB
- Containerized with Docker and Docker Compose
- Automated deployment with custom shell scripts
- Health monitoring and recovery systems

---

**Ready for bulletproof deployment!** 🚀

For questions or support, please open an issue in the repository.