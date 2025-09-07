#!/bin/bash

echo "🌐 Cloud Access Helper for Dealership Application"
echo "================================================"

# Get the public URL from the environment
if [ ! -z "$THEIA_WORKSPACE_ROOT" ]; then
    echo "Detected Theia/Cloud environment"
    
    # Get workspace URL
    WORKSPACE_URL=$(echo $THEIA_WORKSPACE_ROOT | sed 's|/home/project.*||')
    
    if [ ! -z "$WORKSPACE_URL" ]; then
        echo ""
        echo "🌍 Your application should be accessible at:"
        echo "  Main App: ${WORKSPACE_URL}:8000"
        echo "  API:      ${WORKSPACE_URL}:3030"
        echo ""
    fi
fi

# Check if containers are running
echo "📊 Container Status:"
docker-compose ps

echo ""
echo "🔗 Direct URLs (if running locally):"
echo "  Main App: http://localhost:8000"
echo "  API:      http://localhost:3030"

echo ""
echo "⚡ Commands to try:"
echo "  • Check logs: docker-compose logs -f"
echo "  • Restart:    docker-compose restart"
echo "  • Rebuild:    ./quick-deploy.sh"

# Test local connectivity
echo ""
echo "🧪 Testing local connectivity..."
if curl -s http://localhost:8000/ > /dev/null; then
    echo "✅ Django app responding on localhost:8000"
else
    echo "❌ Django app not responding on localhost:8000"
fi

if curl -s http://localhost:3030/ > /dev/null; then
    echo "✅ API responding on localhost:3030"
else
    echo "❌ API not responding on localhost:3030"
fi
