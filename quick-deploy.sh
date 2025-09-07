#!/bin/bash

echo "🚀 Bulletproof Dealership Deployment"
echo "====================================="

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}Starting deployment...${NC}"

# Use docker compose if available, otherwise docker-compose
DOCKER_COMPOSE_CMD="docker compose"
if ! docker compose version &> /dev/null 2>&1; then
    DOCKER_COMPOSE_CMD="docker-compose"
fi

# Clean up and rebuild
echo "Cleaning up existing containers..."
$DOCKER_COMPOSE_CMD down --volumes --remove-orphans 2>/dev/null || true

echo "Building and starting services..."
$DOCKER_COMPOSE_CMD up --build -d

echo "Waiting for services to initialize..."
sleep 30

echo ""
echo -e "${GREEN}✅ Deployment complete!${NC}"
echo ""
echo "Application URLs:"
echo "  🌐 Main App: http://localhost:8000"
echo "  📊 API:      http://localhost:3030" 
echo "  🗄️  MongoDB:  mongodb://localhost:27017"
echo ""
echo "Use './health-check.sh' to verify all services"
