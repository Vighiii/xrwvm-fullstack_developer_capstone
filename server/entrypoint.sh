#!/usr/bin/env bash
set -xe
echo "===> ENTRYPOINT v4 starting"

#!/bin/bash

# Enhanced entrypoint.sh with bulletproof deployment capabilities
# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')] DJANGO ENTRYPOINT:${NC} $1"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1" >&2
}

success() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] SUCCESS:${NC} $1"
}

warning() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING:${NC} $1"
}

# Function to wait for API service with retry logic
wait_for_api() {
    # Skip API health check for local development
    if [ "${DEBUG:-}" = "True" ]; then
        log "Skipping API health check in development mode"
        return 0
    fi
    
    local max_attempts=30
    local attempt=1
    local api_url="http://dealership_api:3030/health"
    
    log "Waiting for dealership API to be ready..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s -f "$api_url" > /dev/null 2>&1; then
            success "API service is ready!"
            return 0
        fi
        
        warning "API not ready (attempt $attempt/$max_attempts). Retrying in 10 seconds..."
        sleep 10
        ((attempt++))
    done
    
    error "API service failed to become ready after $max_attempts attempts"
    return 1
}

# Function to validate Django setup
validate_django() {
    log "Validating Django configuration..."
    
    # Skip deployment check in development mode
    if [ "${DEBUG:-}" = "True" ]; then
        if python manage.py check; then
            success "Django configuration is valid (development mode)"
            return 0
        else
            error "Django configuration validation failed"
            return 1
        fi
    else
        if python manage.py check --deploy; then
            success "Django configuration is valid"
            return 0
        else
            error "Django configuration validation failed"
            return 1
        fi
    fi
}

# Function to collect static files
collect_static() {
    log "Collecting static files..."
    
    if python manage.py collectstatic --noinput --clear; then
        success "Static files collected successfully"
        return 0
    else
        error "Failed to collect static files"
        return 1
    fi
}

# Function to run migrations
run_migrations() {
    log "Running database migrations..."
    
    if python manage.py migrate --noinput; then
        success "Database migrations completed"
        return 0
    else
        error "Database migrations failed"
        return 1
    fi
}

# Function to populate initial data
populate_data() {
    log "Checking if initial data population is needed..."
    
    # Only populate if tables are empty
    if python manage.py shell -c "
from djangoapp.models import CarMake
if not CarMake.objects.exists():
    exit(0)
else:
    exit(1)
"; then
        log "Populating initial data..."
        if python manage.py shell -c "exec(open('djangoapp/populate.py').read())"; then
            success "Initial data populated successfully"
        else
            warning "Initial data population failed, but continuing..."
        fi
    else
        log "Initial data already exists, skipping population"
    fi
}

# Function to create admin user if not exists
create_admin_user() {
    log "Checking for admin user..."
    
    python manage.py shell -c "
from django.contrib.auth.models import User
import os

username = 'emifeaustin0'
email = 'emifeaustin0909@gmail.com'
password = 'admin123'

try:
    admin_user = User.objects.get(username=username)
    print(f'Admin user {username} already exists')
except User.DoesNotExist:
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'Created admin user: {username} with email: {email}')
    
# Ensure admin user has correct email
admin_user = User.objects.get(username=username)
if admin_user.email != email:
    admin_user.email = email
    admin_user.save()
    print(f'Updated admin email to: {email}')
"
    
    if [ $? -eq 0 ]; then
        success "Admin user setup completed"
    else
        warning "Admin user setup failed, but continuing..."
    fi
}

# Main execution
main() {
    log "Starting Django application entrypoint..."
    
    # Set working directory
    cd /app
    
    # Wait for dependencies
    if ! wait_for_api; then
        error "Dependency check failed"
        exit 1
    fi
    
    # Validate Django setup
    if ! validate_django; then
        exit 1
    fi
    
    # Run migrations
    if ! run_migrations; then
        exit 1
    fi
    
    # Collect static files
    if ! collect_static; then
        exit 1
    fi
    
    # Populate initial data
    populate_data
    
    # Create admin user
    create_admin_user
    
    # Start the application
    log "Starting Django development server..."
    success "Django application is ready to serve requests!"
    
    exec python manage.py runserver 0.0.0.0:8000
}

# Run main function
main "$@"

# Hand off to the container's CMD
exec "$@"

