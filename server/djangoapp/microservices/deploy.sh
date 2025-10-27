#!/bin/bash

# Sentiment Analyzer Microservice Deployment Script
# This script builds, pushes, and deploys the sentiment analyzer to IBM Code Engine

set -e  # Exit on any error

echo "=========================================="
echo "Sentiment Analyzer Deployment Script"
echo "=========================================="
echo ""

# Step 1: Navigate to microservices directory
echo "Step 1: Navigating to microservices directory..."
cd "$(dirname "$0")"
pwd
echo ""

# Step 2: Build Docker image
echo "Step 2: Building Docker image..."
echo "Command: docker build . -t us.icr.io/\${SN_ICR_NAMESPACE}/senti_analyzer"
docker build . -t us.icr.io/${SN_ICR_NAMESPACE}/senti_analyzer
echo "✓ Docker image built successfully"
echo ""

# Step 3: Push Docker image to IBM Container Registry
echo "Step 3: Pushing Docker image to IBM Container Registry..."
echo "Command: docker push us.icr.io/\${SN_ICR_NAMESPACE}/senti_analyzer"
docker push us.icr.io/${SN_ICR_NAMESPACE}/senti_analyzer
echo "✓ Docker image pushed successfully"
echo ""

# Step 4: Deploy to Code Engine
echo "Step 4: Deploying to IBM Code Engine..."
echo "Command: ibmcloud ce application create --name sentianalyzer --image us.icr.io/\${SN_ICR_NAMESPACE}/senti_analyzer --registry-secret icr-secret --port 5000"
ibmcloud ce application create --name sentianalyzer \
    --image us.icr.io/${SN_ICR_NAMESPACE}/senti_analyzer \
    --registry-secret icr-secret \
    --port 5000
echo "✓ Application deployed successfully"
echo ""

# Step 5: Get the application URL
echo "Step 5: Retrieving application URL..."
APP_URL=$(ibmcloud ce application get --name sentianalyzer --output json | grep -o '"url":"[^"]*' | cut -d'"' -f4)
echo "✓ Application URL: ${APP_URL}"
echo ""

# Step 6: Test the deployment
echo "Step 6: Testing the deployment..."
echo "Testing welcome endpoint: ${APP_URL}/"
curl -s "${APP_URL}/" || echo "Warning: Could not reach welcome endpoint"
echo ""
echo "Testing sentiment analysis: ${APP_URL}/analyze/Fantastic%20services"
SENTIMENT_RESULT=$(curl -s "${APP_URL}/analyze/Fantastic%20services")
echo "Result: ${SENTIMENT_RESULT}"
echo ""

# Step 7: Display instructions for .env update
echo "=========================================="
echo "Deployment Complete!"
echo "=========================================="
echo ""
echo "IMPORTANT: Update your .env file with the following:"
echo ""
echo "sentiment_analyzer_url=${APP_URL}/"
echo ""
echo "Note: Make sure to include the trailing slash (/) at the end of the URL"
echo ""
echo "To update the .env file, run:"
echo "echo 'sentiment_analyzer_url=${APP_URL}/' >> server/djangoapp/.env"
echo ""
echo "Or manually edit server/djangoapp/.env and add/update the line:"
echo "sentiment_analyzer_url=${APP_URL}/"
echo ""
echo "=========================================="
