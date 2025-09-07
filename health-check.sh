#!/bin/bash

# Health Check Script for Dealership Application
# Monitors all services and provides detailed health status

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🏥 Health Check - Dealership Application${NC}"
echo "=============================================="

# Function to check if service is responsive
check_service() {
    local service_name=$1
    local url=$2
    local expected_content=$3
    
    echo -n "Checking $service_name... "
    
    if curl -s --max-time 10 "$url" | grep -q "$expected_content" 2>/dev/null; then
        echo -e "${GREEN}✅ Healthy${NC}"
        return 0
    else
        echo -e "${RED}❌ Unhealthy${NC}"
        return 1
    fi
}

# Function to check MongoDB
check_mongodb() {
    echo -n "Checking MongoDB... "
    
    if docker exec dealership_mongodb mongosh --quiet --eval "db.adminCommand('ping').ok" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Healthy${NC}"
        return 0
    else
        echo -e "${RED}❌ Unhealthy${NC}"
        return 1
    fi
}

# Function to check container status
check_containers() {
    echo -e "\n${BLUE}Container Status:${NC}"
    
    local containers=("dealership_mongodb" "dealership_api" "dealership_django")
    local all_running=true
    
    for container in "${containers[@]}"; do
        if docker ps --filter "name=$container" --filter "status=running" | grep -q "$container"; then
            echo -e "  $container: ${GREEN}Running${NC}"
        else
            echo -e "  $container: ${RED}Not Running${NC}"
            all_running=false
        fi
    done
    
    return $all_running
}

# Main health check
echo -e "\n${BLUE}Service Health Status:${NC}"

# Check individual services
health_status=0

check_mongodb || ((health_status++))
check_service "API Service" "http://localhost:3030/" "Express" || ((health_status++))
check_service "Django App" "http://localhost:8000/" "dealership" || ((health_status++))

# Check containers
echo ""
if ! check_containers; then
    ((health_status++))
fi

# Show detailed service info
echo -e "\n${BLUE}Detailed Service Information:${NC}"

# API endpoints
echo -e "\n${BLUE}API Endpoints:${NC}"
echo -n "  /dealerships: "
if curl -s "http://localhost:3030/dealerships" >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Working${NC}"
else
    echo -e "${RED}❌ Failed${NC}"
    ((health_status++))
fi

echo -n "  /reviews: "
if curl -s "http://localhost:3030/reviews" >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Working${NC}"
else
    echo -e "${RED}❌ Failed${NC}"
    ((health_status++))
fi

# Django endpoints
echo -e "\n${BLUE}Django Endpoints:${NC}"
echo -n "  /: "
if curl -s "http://localhost:8000/" >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Working${NC}"
else
    echo -e "${RED}❌ Failed${NC}"
    ((health_status++))
fi

echo -n "  /djangoapp/: "
if curl -s "http://localhost:8000/djangoapp/" >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Working${NC}"
else
    echo -e "${RED}❌ Failed${NC}"
    ((health_status++))
fi

# Summary
echo ""
echo "=============================================="
if [ $health_status -eq 0 ]; then
    echo -e "${GREEN}🎉 All systems healthy!${NC}"
    exit 0
else
    echo -e "${RED}⚠️  $health_status issue(s) detected${NC}"
    echo ""
    echo "Troubleshooting commands:"
    echo "  docker-compose logs"
    echo "  docker-compose ps"
    echo "  docker-compose restart"
    exit 1
fi
