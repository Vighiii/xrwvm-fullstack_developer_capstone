#!/bin/bash

# Script to update .env file with Code Engine deployment URL

set -e

echo "=========================================="
echo "Update .env with Sentiment Analyzer URL"
echo "=========================================="
echo ""

# Get the application URL from Code Engine
echo "Retrieving application URL from Code Engine..."
APP_URL=$(ibmcloud ce application get --name sentianalyzer --output json | grep -o '"url":"[^"]*' | cut -d'"' -f4)

if [ -z "$APP_URL" ]; then
    echo "❌ Error: Could not retrieve application URL"
    echo "Please ensure the application is deployed:"
    echo "  ibmcloud ce application get --name sentianalyzer"
    exit 1
fi

echo "✓ Application URL found: ${APP_URL}"
echo ""

# Path to .env file
ENV_FILE="../.env"

# Check if .env file exists
if [ ! -f "$ENV_FILE" ]; then
    echo "Creating new .env file..."
    touch "$ENV_FILE"
fi

# Check if sentiment_analyzer_url already exists in .env
if grep -q "^sentiment_analyzer_url=" "$ENV_FILE"; then
    echo "Updating existing sentiment_analyzer_url in .env..."
    # Use sed to replace the line (works on both macOS and Linux)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s|^sentiment_analyzer_url=.*|sentiment_analyzer_url=${APP_URL}/|" "$ENV_FILE"
    else
        # Linux
        sed -i "s|^sentiment_analyzer_url=.*|sentiment_analyzer_url=${APP_URL}/|" "$ENV_FILE"
    fi
else
    echo "Adding sentiment_analyzer_url to .env..."
    echo "sentiment_analyzer_url=${APP_URL}/" >> "$ENV_FILE"
fi

echo "✓ .env file updated successfully"
echo ""
echo "Current .env configuration:"
grep "sentiment_analyzer_url=" "$ENV_FILE"
echo ""
echo "=========================================="
echo "Configuration Complete!"
echo "=========================================="
echo ""
echo "You can now test the integration from your Django app."
echo ""
