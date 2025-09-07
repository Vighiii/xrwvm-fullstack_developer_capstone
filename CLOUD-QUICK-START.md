# 🌐 Cloud IDE Quick Start

## 🚀 One-Command Startup

```bash
# Clone and start (first time)
git clone https://github.com/emiflair/xrwvm-fullstack_developer_capstone.git
cd xrwvm-fullstack_developer_capstone
./start-cloud.sh
```

## 🔄 Daily Startup (after first setup)

```bash
cd xrwvm-fullstack_developer_capstone
./start-cloud.sh
```

## 🌍 Platform-Specific Access

### GitHub Codespaces
- Ports are auto-forwarded
- Access via: `https://[codespace-name]-8000.githubpreview.dev`

### Gitpod  
- Make ports 8000 & 3030 **PUBLIC** in Ports tab
- Access via: `https://8000-[workspace-id].ws-[region].gitpod.io`

### IBM Cloud / Theia
- Configure port forwarding in IDE settings
- Use provided external URLs

### Replit
- Ports auto-detected and forwarded
- Access via Replit's webview URLs

## 🔧 Troubleshooting

```bash
# View logs
docker-compose logs -f

# Restart services  
docker-compose restart

# Full reset
docker-compose down -v && ./start-cloud.sh
```

**📖 For detailed instructions, see: [CLOUD-STARTUP-GUIDE.md](./CLOUD-STARTUP-GUIDE.md)**
