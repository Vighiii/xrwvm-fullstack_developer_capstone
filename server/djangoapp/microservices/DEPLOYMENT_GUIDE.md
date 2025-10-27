# Sentiment Analyzer Microservice Deployment Guide

This guide will help you deploy the sentiment analysis microservice to IBM Code Engine.

## Prerequisites

Before starting, ensure you have:
- IBM Cloud CLI installed
- Docker installed and running
- Logged into IBM Cloud CLI (`ibmcloud login`)
- Code Engine plugin installed (`ibmcloud plugin install code-engine`)
- Environment variable `SN_ICR_NAMESPACE` set to your IBM Container Registry namespace

## Deployment Steps

### Option 1: Automated Deployment (Recommended)

1. **Make the deployment script executable:**

   ```bash
   chmod +x server/djangoapp/microservices/deploy.sh
   ```

2. **Run the deployment script:**
   ```bash
   cd server/djangoapp/microservices
   ./deploy.sh
   ```

3. **Follow the on-screen instructions** to update your `.env` file with the generated URL.

### Option 2: Manual Deployment

#### Step 1: Navigate to Microservices Directory

```bash
cd server/djangoapp/microservices
```

#### Step 2: Build Docker Image

```bash
docker build . -t us.icr.io/${SN_ICR_NAMESPACE}/senti_analyzer
```

This command:

- Builds a Docker image from the Dockerfile
- Tags it with your IBM Container Registry namespace
- Names it `senti_analyzer`

#### Step 3: Push Docker Image

```bash
docker push us.icr.io/${SN_ICR_NAMESPACE}/senti_analyzer
```

This uploads your Docker image to IBM Container Registry.

#### Step 4: Deploy to Code Engine

```bash
ibmcloud ce application create --name sentianalyzer \
    --image us.icr.io/${SN_ICR_NAMESPACE}/senti_analyzer \
    --registry-secret icr-secret \
    --port 5000
```

This command:

- Creates a new Code Engine application named `sentianalyzer`
- Uses the Docker image you just pushed
- Configures it to use port 5000
- Uses the `icr-secret` for authentication

#### Step 5: Get Application URL

```bash
ibmcloud ce application get --name sentianalyzer
```

Look for the URL in the output. It will look something like:

```
https://sentianalyzer.xxxxxxxxx.us-south.codeengine.appdomain.cloud
```

#### Step 6: Test the Deployment

Test the welcome endpoint:

```bash
curl https://your-app-url/
```

Expected response:

```
Welcome to the Sentiment Analyzer. Use /analyze/text to get the sentiment
```

Test sentiment analysis:

```bash
curl https://your-app-url/analyze/Fantastic%20services
```

Expected response:

```json
{"sentiment": "positive"}
```

#### Step 7: Take Screenshot

Open your browser and navigate to:

```
https://your-app-url/analyze/Fantastic%20services
```

Take a screenshot showing:

- The URL in the address bar
- The JSON response with positive sentiment

Save it as `sentiment_analyzer.png` or `sentiment_analyzer.jpeg`

#### Step 8: Update .env File

Edit `server/djangoapp/.env` and add/update:

```
sentiment_analyzer_url=https://your-app-url/
```

**IMPORTANT:** Make sure to include the trailing slash `/` at the end!

## Verification

After updating the `.env` file, verify the integration:

1. **Check the restapis.py file** (already implemented):

   ```python
   def analyze_review_sentiments(text):
       request_url = sentiment_analyzer_url + "analyze/" + text
       try:
           response = requests.get(request_url)
           return response.json()
       except Exception as err:
           print(f"Unexpected {err=}, {type(err)=}")
           print("Network exception occurred")
           return {"sentiment": "neutral"}
   ```

2. **Test from Django app:**

   ```python
   from djangoapp.restapis import analyze_review_sentiments
   result = analyze_review_sentiments("This is amazing")
   print(result)  # Should print: {'sentiment': 'positive'}
   ```

## Troubleshooting

### Docker Build Fails

- Ensure Docker is running
- Check that you're in the correct directory (`server/djangoapp/microservices`)
- Verify the Dockerfile exists

### Docker Push Fails

- Verify you're logged into IBM Cloud: `ibmcloud login`
- Check your Container Registry namespace: `echo $SN_ICR_NAMESPACE`
- Ensure you have permissions to push to the registry

### Code Engine Deployment Fails

- Verify Code Engine plugin is installed: `ibmcloud plugin list`
- Check you're targeting the correct region: `ibmcloud target`
- Ensure the `icr-secret` exists in your Code Engine project

### Application Not Responding

- Check application status: `ibmcloud ce application get --name sentianalyzer`
- View logs: `ibmcloud ce application logs --name sentianalyzer`
- Verify the port is set to 5000

### Sentiment Analysis Returns Wrong Results

- Test the endpoint directly in browser
- Check the NLTK vader_lexicon is properly loaded
- Review application logs for errors

## Useful Commands

### View Application Details

```bash
ibmcloud ce application get --name sentianalyzer
```

### View Application Logs

```bash
ibmcloud ce application logs --name sentianalyzer --follow
```

### Update Application (if needed)

```bash
ibmcloud ce application update --name sentianalyzer \
    --image us.icr.io/${SN_ICR_NAMESPACE}/senti_analyzer
```

### Delete Application

```bash
ibmcloud ce application delete --name sentianalyzer
```

### List All Applications

```bash
ibmcloud ce application list
```

## Architecture

```
┌─────────────────┐
│  Django App     │
│  (restapis.py)  │
└────────┬────────┘
         │ HTTP Request
         │ GET /analyze/<text>
         ▼
┌─────────────────┐
│  Code Engine    │
│  Microservice   │
│  (Flask App)    │
└────────┬────────┘
         │ NLTK Analysis
         ▼
┌─────────────────┐
│  Sentiment      │
│  Response       │
│  {"sentiment":  │
│   "positive"}   │
└─────────────────┘
```

## Files Overview

- **app.py**: Flask application with sentiment analysis endpoints
- **Dockerfile**: Container configuration for deployment
- **requirements.txt**: Python dependencies (Flask, nltk)
- **sentiment/vader_lexicon.zip**: NLTK sentiment analysis data
- **deploy.sh**: Automated deployment script
- **DEPLOYMENT_GUIDE.md**: This guide

## Next Steps

After successful deployment:

1. ✅ Verify the microservice is accessible
2. ✅ Update the `.env` file with the deployment URL
3. ✅ Test the integration from your Django application
4. ✅ Take a screenshot for documentation
5. ✅ Commit your changes (excluding `.env` file)

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review IBM Code Engine documentation
3. Check application logs for detailed error messages
4. Verify all prerequisites are met
