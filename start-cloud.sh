#!/bin/bash

echo "🚀 Starting Dealership Application in Cloud IDE"
echo "=============================================="

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Error: docker-compose.yml not found!"
    echo "Please run this script from the project root directory."
    exit 1
fi

# Make all scripts executable
echo "🔧 Setting up permissions..."
chmod +x *.sh

# Start the application
echo "🌐 Starting all services..."
docker-compose up -d

# Wait for services to start
echo "⏳ Waiting for services to initialize..."
sleep 10

# Check service status
echo "🔍 Checking service status..."
docker-compose ps

# Test local connectivity
echo "🧪 Testing service connectivity..."
echo -n "Django App: "
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/ | grep -q "200\|302"; then
    echo "✅ Running"
else
    echo "❌ Not responding"
fi

echo -n "API Service: "
if curl -s http://localhost:3030/health | grep -q "ok"; then
    echo "✅ Healthy"
else
    echo "❌ Not healthy"
fi

echo ""
echo "🎉 Application started successfully!"
echo ""
echo "📋 Next Steps:"
echo "1. Configure port forwarding in your cloud IDE:"
echo "   - Port 8000 (Django App)"
echo "   - Port 3030 (API Service)"
echo ""
echo "2. Make ports PUBLIC (not just open) in your IDE settings"
echo ""
echo "3. Access your application using the URLs provided by your cloud IDE"
echo ""
echo "🔧 Useful commands:"
echo "   View logs:     docker-compose logs -f"
echo "   Stop services: docker-compose down"
echo "   Restart:       docker-compose restart"
echo ""
echo "❓ Need help? Run: ./cloud-setup-guide.sh"
