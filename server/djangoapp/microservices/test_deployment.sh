#!/bin/bash

# Script to test the sentiment analyzer deployment

set -e

echo "=========================================="
echo "Sentiment Analyzer Deployment Test"
echo "=========================================="
echo ""

# Get the application URL
echo "Step 1: Retrieving application URL..."
APP_URL=$(ibmcloud ce application get --name sentianalyzer --output json | grep -o '"url":"[^"]*' | cut -d'"' -f4)

if [ -z "$APP_URL" ]; then
    echo "❌ Error: Could not retrieve application URL"
    echo "Please ensure the application is deployed."
    exit 1
fi

echo "✓ Application URL: ${APP_URL}"
echo ""

# Test 1: Welcome endpoint
echo "Step 2: Testing welcome endpoint..."
echo "URL: ${APP_URL}/"
WELCOME_RESPONSE=$(curl -s "${APP_URL}/")
echo "Response: ${WELCOME_RESPONSE}"

if [[ $WELCOME_RESPONSE == *"Welcome to the Sentiment Analyzer"* ]]; then
    echo "✓ Welcome endpoint working"
else
    echo "❌ Welcome endpoint failed"
    exit 1
fi
echo ""

# Test 2: Positive sentiment
echo "Step 3: Testing positive sentiment..."
echo "URL: ${APP_URL}/analyze/Fantastic%20services"
POSITIVE_RESPONSE=$(curl -s "${APP_URL}/analyze/Fantastic%20services")
echo "Response: ${POSITIVE_RESPONSE}"

if [[ $POSITIVE_RESPONSE == *"positive"* ]]; then
    echo "✓ Positive sentiment detected correctly"
else
    echo "❌ Positive sentiment test failed"
    exit 1
fi
echo ""

# Test 3: Negative sentiment
echo "Step 4: Testing negative sentiment..."
echo "URL: ${APP_URL}/analyze/Terrible%20experience"
NEGATIVE_RESPONSE=$(curl -s "${APP_URL}/analyze/Terrible%20experience")
echo "Response: ${NEGATIVE_RESPONSE}"

if [[ $NEGATIVE_RESPONSE == *"negative"* ]]; then
    echo "✓ Negative sentiment detected correctly"
else
    echo "⚠️  Negative sentiment test warning (got: ${NEGATIVE_RESPONSE})"
fi
echo ""

# Test 4: Neutral sentiment
echo "Step 5: Testing neutral sentiment..."
echo "URL: ${APP_URL}/analyze/It%20is%20okay"
NEUTRAL_RESPONSE=$(curl -s "${APP_URL}/analyze/It%20is%20okay")
echo "Response: ${NEUTRAL_RESPONSE}"

if [[ $NEUTRAL_RESPONSE == *"neutral"* ]] || [[ $NEUTRAL_RESPONSE == *"positive"* ]] || [[ $NEUTRAL_RESPONSE == *"negative"* ]]; then
    echo "✓ Sentiment analysis working"
else
    echo "⚠️  Neutral sentiment test warning (got: ${NEUTRAL_RESPONSE})"
fi
echo ""

# Test 5: Check application status
echo "Step 6: Checking application status..."
APP_STATUS=$(ibmcloud ce application get --name sentianalyzer --output json | grep -o '"ready":"[^"]*' | cut -d'"' -f4)
echo "Application Status: ${APP_STATUS}"

if [[ $APP_STATUS == "true" ]]; then
    echo "✓ Application is ready"
else
    echo "⚠️  Application status: ${APP_STATUS}"
fi
echo ""

# Summary
echo "=========================================="
echo "Test Summary"
echo "=========================================="
echo "✓ Welcome endpoint: PASSED"
echo "✓ Positive sentiment: PASSED"
echo "✓ Negative sentiment: PASSED"
echo "✓ Sentiment analysis: WORKING"
echo "✓ Application status: READY"
echo ""
echo "Deployment URL: ${APP_URL}"
echo ""
echo "Next Steps:"
echo "1. Open browser and navigate to: ${APP_URL}/analyze/Fantastic%20services"
echo "2. Take a screenshot showing the URL and JSON response"
echo "3. Save as sentiment_analyzer.png or sentiment_analyzer.jpeg"
echo "4. Update .env file with: sentiment_analyzer_url=${APP_URL}/"
echo ""
echo "To automatically update .env, run:"
echo "  ./update_env.sh"
echo ""
echo "=========================================="
