#!/bin/bash

echo "🌐 Cloud Deployment Script for Dealership Application"
echo "===================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${PURPLE}$1${NC}"
}

# Detect cloud environment
detect_cloud_env() {
    print_header "🔍 Detecting Cloud Environment"
    
    if [ ! -z "$GITPOD_WORKSPACE_URL" ]; then
        CLOUD_ENV="gitpod"
        BASE_URL="$GITPOD_WORKSPACE_URL"
        print_status "Detected Gitpod environment"
    elif [ ! -z "$CODESPACE_NAME" ]; then
        CLOUD_ENV="codespaces"
        BASE_URL="https://${CODESPACE_NAME}-8000.${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN}"
        print_status "Detected GitHub Codespaces environment"
    elif [ ! -z "$THEIA_WORKSPACE_ROOT" ]; then
        CLOUD_ENV="theia"
        # Extract workspace URL from the current environment
        WORKSPACE_ID=$(hostname | cut -d'-' -f1)
        BASE_URL="https://${WORKSPACE_ID}-8000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai"
        print_status "Detected Theia/IBM Cloud environment"
    elif [ ! -z "$REPL_SLUG" ]; then
        CLOUD_ENV="replit"
        BASE_URL="https://${REPL_SLUG}.${REPL_OWNER}.repl.co"
        print_status "Detected Replit environment"
    else
        CLOUD_ENV="unknown"
        print_warning "Could not detect cloud environment, using default configuration"
    fi
}

# Clean and rebuild containers
rebuild_for_cloud() {
    print_header "🏗️ Rebuilding for Cloud Deployment"
    
    # Use docker compose if available, otherwise docker-compose
    DOCKER_COMPOSE_CMD="docker compose"
    if ! docker compose version &> /dev/null 2>&1; then
        DOCKER_COMPOSE_CMD="docker-compose"
    fi
    
    print_status "Stopping existing containers..."
    $DOCKER_COMPOSE_CMD down --volumes --remove-orphans 2>/dev/null || true
    
    print_status "Removing old images..."
    docker rmi -f $(docker images -q "*dealership*" "*xrwvm*" 2>/dev/null) 2>/dev/null || true
    
    print_status "Building services for cloud deployment..."
    $DOCKER_COMPOSE_CMD build --no-cache
    
    print_status "Starting services..."
    $DOCKER_COMPOSE_CMD up -d
    
    print_status "Waiting for services to initialize..."
    sleep 45
}

# Test cloud accessibility
test_cloud_access() {
    print_header "🧪 Testing Cloud Accessibility"
    
    # Test local connectivity first
    if curl -s --max-time 10 http://localhost:8000/ > /dev/null; then
        print_success "Django app responding locally ✓"
    else
        print_error "Django app not responding locally ✗"
        return 1
    fi
    
    if curl -s --max-time 10 http://localhost:3030/ > /dev/null; then
        print_success "API responding locally ✓"
    else
        print_error "API not responding locally ✗"
        return 1
    fi
    
    return 0
}

# Show cloud URLs
show_cloud_urls() {
    print_header "🌍 Cloud Access Information"
    
    echo ""
    echo -e "${GREEN}✅ Your application is ready for cloud access!${NC}"
    echo ""
    
    case $CLOUD_ENV in
        "gitpod")
            DJANGO_URL="${GITPOD_WORKSPACE_URL/https:\/\//https://8000-}"
            API_URL="${GITPOD_WORKSPACE_URL/https:\/\//https://3030-}"
            ;;
        "codespaces")
            DJANGO_URL="https://${CODESPACE_NAME}-8000.${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN}"
            API_URL="https://${CODESPACE_NAME}-3030.${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN}"
            ;;
        "theia")
            WORKSPACE_ID=$(hostname | cut -d'-' -f1)
            DJANGO_URL="https://${WORKSPACE_ID}-8000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai"
            API_URL="https://${WORKSPACE_ID}-3030.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai"
            ;;
        "replit")
            DJANGO_URL="https://${REPL_SLUG}-8000.${REPL_OWNER}.repl.co"
            API_URL="https://${REPL_SLUG}-3030.${REPL_OWNER}.repl.co"
            ;;
        *)
            DJANGO_URL="Check your IDE's port forwarding for port 8000"
            API_URL="Check your IDE's port forwarding for port 3030"
            ;;
    esac
    
    echo -e "${BLUE}🌐 Cloud URLs:${NC}"
    echo "  Main App:  $DJANGO_URL"
    echo "  API:       $API_URL"
    echo ""
    
    echo -e "${BLUE}📱 Local URLs (for testing):${NC}"
    echo "  Main App:  http://localhost:8000"
    echo "  API:       http://localhost:3030"
    echo "  MongoDB:   mongodb://localhost:27017"
    echo ""
    
    echo -e "${BLUE}⚙️ Port Forwarding Setup:${NC}"
    echo "  Make sure these ports are exposed in your IDE:"
    echo "  • Port 8000 (Django Application)"
    echo "  • Port 3030 (API Service)"
    echo "  • Set visibility to 'Public' or 'Open to Internet'"
    echo ""
    
    echo -e "${BLUE}🔧 Troubleshooting:${NC}"
    echo "  • Wait 30-60 seconds for ports to become available"
    echo "  • Check IDE's 'Ports' tab and ensure ports are public"
    echo "  • Try refreshing the browser"
    echo "  • Use IDE's 'Open in Browser' feature"
    echo ""
}

# Main execution
main() {
    echo ""
    detect_cloud_env
    rebuild_for_cloud
    
    if test_cloud_access; then
        show_cloud_urls
        print_success "🎉 Cloud deployment completed successfully!"
    else
        print_error "❌ Deployment issues detected. Check container logs:"
        echo "  docker-compose logs -f"
        exit 1
    fi
}

# Run main function
main "$@"
