# 🌐 Cloud IDE Startup Guide for Dealership Application

## 🚀 Quick Start Commands

### **1. Clone and Setup (First Time)**
```bash
# Clone the repository
git clone https://github.com/emiflair/xrwvm-fullstack_developer_capstone.git
cd xrwvm-fullstack_developer_capstone

# Make scripts executable
chmod +x *.sh

# Start the application
./cloud-deploy.sh
```

### **2. Daily Startup (After First Setup)**
```bash
# Navigate to project directory
cd xrwvm-fullstack_developer_capstone

# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs (optional)
docker-compose logs -f
```

## 🔧 Platform-Specific Instructions

### **GitHub Codespaces**
1. **Open Repository**: Click "Code" → "Create codespace on main"
2. **Wait for Setup**: Codespaces will automatically install Docker
3. **Run Commands**:
   ```bash
   ./cloud-deploy.sh
   ```
4. **Access Application**: Codespaces will automatically forward ports
   - Django App: `https://[codespace-name]-8000.githubpreview.dev`
   - API: `https://[codespace-name]-3030.githubpreview.dev`

### **Gitpod**
1. **Open in Gitpod**: `https://gitpod.io/#https://github.com/emiflair/xrwvm-fullstack_developer_capstone`
2. **Run Commands**:
   ```bash
   ./cloud-deploy.sh
   ```
3. **Make Ports Public**:
   - Go to "Ports" tab in Gitpod
   - Make ports 8000 and 3030 "Public"
4. **Access URLs**: Gitpod will provide the public URLs

### **IBM Cloud (Theia IDE)**
1. **Upload Project** or clone via terminal
2. **Run Commands**:
   ```bash
   ./cloud-deploy.sh
   ```
3. **Configure Port Forwarding** in Theia settings
4. **Access**: Use the provided external URLs

### **Replit**
1. **Import Repository**: "Create" → "Import from GitHub"
2. **Run Commands**:
   ```bash
   ./cloud-deploy.sh
   ```
3. **Configure Ports**: Replit auto-detects and forwards ports
4. **Access**: Use Replit's provided URLs

## 📋 Step-by-Step Startup Process

### **Step 1: Initial Setup**
```bash
# Make sure you're in the project root
ls -la

# You should see: cloud-deploy.sh, docker-compose.yml, README.md

# Make scripts executable
chmod +x cloud-deploy.sh cloud-setup-guide.sh cloud-access.sh
```

### **Step 2: Start Application**
```bash
# One-command deployment (recommended)
./cloud-deploy.sh

# OR manual startup
docker-compose up --build -d
```

### **Step 3: Verify Services**
```bash
# Check all containers are running
docker-compose ps

# Test local access
curl http://localhost:8000/      # Django app
curl http://localhost:3030/health # API health check
```

### **Step 4: Configure Cloud Access**
```bash
# Get cloud-specific URLs and instructions
./cloud-setup-guide.sh

# Quick cloud access helper
./cloud-access.sh
```

## 🔍 Troubleshooting Commands

### **Check Container Status**
```bash
docker-compose ps
docker-compose logs dealership_django
docker-compose logs dealership_api
docker-compose logs dealership_mongodb
```

### **Restart Services**
```bash
# Restart all services
docker-compose restart

# Restart specific service
docker-compose restart dealership_django
```

### **Clean Restart**
```bash
# Stop and remove everything
docker-compose down -v

# Rebuild and start fresh
docker-compose up --build -d
```

### **Health Checks**
```bash
# Django health
curl -I http://localhost:8000/

# API health
curl http://localhost:3030/health

# MongoDB connection test
docker-compose exec dealership_mongodb mongosh --eval "db.adminCommand('ping')"
```

## 🌐 Port Configuration

| Service | Internal Port | External Port | URL |
|---------|---------------|---------------|-----|
| Django  | 8000 | 8000 | `http://localhost:8000` |
| API     | 3030 | 3030 | `http://localhost:3030` |
| MongoDB | 27017 | 27017 | `mongodb://localhost:27017` |

## 🚨 Common Issues & Solutions

### **Issue: "Port already in use"**
```bash
# Kill processes using the ports
sudo lsof -ti:8000 | xargs kill -9
sudo lsof -ti:3030 | xargs kill -9
docker-compose down -v
```

### **Issue: "Docker not found"**
```bash
# Most cloud IDEs have Docker pre-installed
# If not, contact your cloud provider support
docker --version
```

### **Issue: "Permission denied"**
```bash
# Make scripts executable
chmod +x *.sh

# Run with explicit bash
bash cloud-deploy.sh
```

### **Issue: "Can't access from browser"**
1. **Check port forwarding** in your cloud IDE
2. **Make ports public** (not just open)
3. **Use HTTPS URLs** if provided by cloud IDE
4. **Check firewall settings** in cloud environment

## 🎯 Production Deployment Commands

### **For Cloud Platforms (AWS, Google Cloud, Azure)**
```bash
# Use Docker Compose directly
docker-compose up -d

# Or with custom environment
DJANGO_ENV=production docker-compose up -d
```

### **For Kubernetes**
```bash
# Convert to Kubernetes manifests (if needed)
kompose convert

# Deploy to cluster
kubectl apply -f .
```

## 📱 Quick Access URLs

After startup, your application will be available at:
- **Main Application**: Your cloud IDE will provide the Django URL (port 8000)
- **API Endpoints**: Your cloud IDE will provide the API URL (port 3030)
- **API Health Check**: `[API_URL]/health`

## 🆘 Get Help

If you encounter issues:
1. **Run diagnostics**: `./cloud-setup-guide.sh`
2. **Check logs**: `docker-compose logs -f`
3. **Restart services**: `docker-compose restart`
4. **Full reset**: `docker-compose down -v && ./cloud-deploy.sh`

---
**Happy Coding! 🚀**
