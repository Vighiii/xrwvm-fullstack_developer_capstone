#!/bin/bash

echo "🚀 Simple Start - Dealership Application"
echo "========================================"

# Use docker compose if available, otherwise docker-compose
DOCKER_COMPOSE_CMD="docker compose"
if ! docker compose version &> /dev/null 2>&1; then
    DOCKER_COMPOSE_CMD="docker-compose"
fi

echo "Starting services..."
$DOCKER_COMPOSE_CMD up -d

echo "Waiting for services to initialize..."
sleep 30

echo ""
echo "✅ Services started!"
echo ""
echo "Application URLs:"
echo "  🌐 Main App: http://localhost:8000"
echo "  📊 API:      http://localhost:3030"
echo "  🗄️  MongoDB:  mongodb://localhost:27017"
echo ""
echo "Use 'docker-compose logs -f' to view logs"
echo "Use './health-check.sh' to check status"
