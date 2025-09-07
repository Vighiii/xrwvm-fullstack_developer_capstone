#!/bin/bash

# Local Development Stop Script
# Stop the dealership application services

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🛑 Stopping Dealership Management System${NC}"
echo "==========================================="

# Change to script directory
cd "$(dirname "$0")" || exit 1

# Use docker compose if available, otherwise docker-compose
DOCKER_COMPOSE_CMD="docker compose"
if ! docker compose version &> /dev/null 2>&1; then
    DOCKER_COMPOSE_CMD="docker-compose"
fi

echo -e "${BLUE}Stopping services...${NC}"
$DOCKER_COMPOSE_CMD down

echo -e "${GREEN}✅ All services stopped successfully!${NC}"
echo ""
echo "To start again, run: ./simple-start.sh"
