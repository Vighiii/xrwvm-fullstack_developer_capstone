# Dealership Management System - Development Makefile
# Provides easy commands for common development tasks

.PHONY: help build start stop restart logs clean test admin shell

# Default target
help:
	@echo "🚗 Dealership Management System - Development Commands"
	@echo "======================================================"
	@echo ""
	@echo "Available commands:"
	@echo "  make start     - Start all services (equivalent to docker-compose up -d)"
	@echo "  make stop      - Stop all services"
	@echo "  make restart   - Restart all services"
	@echo "  make build     - Build all Docker images"
	@echo "  make logs      - View logs from all services"
	@echo "  make clean     - Stop services and remove all volumes (fresh start)"
	@echo "  make test      - Run application health checks"
	@echo "  make admin     - Create Django admin user"
	@echo "  make shell     - Open Django shell"
	@echo "  make help      - Show this help message"
	@echo ""
	@echo "Application URLs:"
	@echo "  Web App:  http://localhost:8000"
	@echo "  API:      http://localhost:3030"
	@echo "  Admin:    http://localhost:8000/admin/"

# Start all services
start:
	@echo "🚀 Starting Dealership Management System..."
	docker-compose up -d
	@echo "✅ Services started! Access the app at http://localhost:8000"

# Stop all services
stop:
	@echo "🛑 Stopping all services..."
	docker-compose down

# Restart all services
restart:
	@echo "🔄 Restarting all services..."
	docker-compose restart

# Build all Docker images
build:
	@echo "🏗️  Building Docker images..."
	docker-compose build --no-cache

# View logs from all services
logs:
	@echo "📋 Viewing logs (press Ctrl+C to exit)..."
	docker-compose logs -f

# Clean everything (stop and remove volumes)
clean:
	@echo "🧹 Cleaning up (this will remove all data)..."
	@read -p "Are you sure? This will delete all data [y/N]: " confirm && [ "$${confirm:-N}" = "y" ]
	docker-compose down -v
	docker system prune -f
	@echo "✅ Cleanup complete!"

# Run application health checks
test:
	@echo "🧪 Running application health checks..."
	@echo "Testing Django application..."
	@curl -f http://localhost:8000/ > /dev/null && echo "✅ Django: OK" || echo "❌ Django: FAILED"
	@echo "Testing API service..."
	@curl -f http://localhost:3030/health > /dev/null && echo "✅ API: OK" || echo "❌ API: FAILED"
	@echo "Testing admin panel..."
	@curl -f http://localhost:8000/admin/ > /dev/null && echo "✅ Admin: OK" || echo "❌ Admin: FAILED"

# Create Django admin user
admin:
	@echo "👤 Creating Django admin user..."
	docker-compose exec dealership_django python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin123')"
	@echo "✅ Admin user created: admin/admin123"

# Open Django shell
shell:
	@echo "🐍 Opening Django shell..."
	docker-compose exec dealership_django python manage.py shell

# Production deployment
deploy-prod:
	@echo "🚀 Deploying to production..."
	docker-compose -f docker-compose.prod.yml up -d --build
	@echo "✅ Production deployment complete!"

# Check Docker and Docker Compose
check-deps:
	@echo "🔍 Checking dependencies..."
	@which docker > /dev/null && echo "✅ Docker: Installed" || echo "❌ Docker: Not found"
	@which docker-compose > /dev/null && echo "✅ Docker Compose: Installed" || echo "❌ Docker Compose: Not found"
	@docker info > /dev/null 2>&1 && echo "✅ Docker: Running" || echo "❌ Docker: Not running"
