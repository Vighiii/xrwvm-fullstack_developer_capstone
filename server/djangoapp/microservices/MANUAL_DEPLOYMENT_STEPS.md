# Manual Deployment Steps - Execute These Commands

Since Docker and IBM Cloud CLI commands need to be run from your terminal with proper credentials, follow these steps:

## Prerequisites Check

1.  **Ensure Docker Desktop is running**
    *   Open Docker Desktop application
    *   Wait until it shows "Docker Desktop is running"
2.  **Verify Docker is accessible**
    ```bash
    docker --version
    docker ps
    ```
3.  **Verify IBM Cloud CLI is logged in**
    ```bash
    ibmcloud target
    ```
4.  **Check environment variable**
    ```bash
    echo $SN_ICR_NAMESPACE
    ```
    If empty, set it:
    ```bash
    export SN_ICR_NAMESPACE=your-namespace-here
    ```

---

## Step-by-Step Deployment Commands

### Step 1: Navigate to Microservices Directory

```bash
cd /Users/Salama/IBM/xrwvm-fullstack_developer_capstone/server/djangoapp/microservices
```

### Step 2: Build Docker Image

```bash
docker build . -t us.icr.io/${SN_ICR_NAMESPACE}/senti_analyzer
```

**Expected Output:**

```
[+] Building 45.2s (10/10) FINISHED
...
Successfully built [image-id]
Successfully tagged us.icr.io/[namespace]/senti_analyzer:latest
```

**If this fails:**

*   Ensure Docker Desktop is running
*   Check Dockerfile exists in current directory
*   Verify you have internet connection for downloading base image

### Step 3: Push Docker Image to IBM Container Registry

```bash
docker push us.icr.io/${SN_ICR_NAMESPACE}/senti_analyzer
```

**Expected Output:**

```
The push refers to repository [us.icr.io/[namespace]/senti_analyzer]
...
latest: digest: sha256:... size: ...
```

**If this fails:**

*   Ensure you're logged into IBM Cloud: `ibmcloud login`
*   Verify Container Registry access: `ibmcloud cr login`
*   Check namespace exists: `ibmcloud cr namespace-list`

### Step 4: Deploy to Code Engine

```bash
ibmcloud ce application create --name sentianalyzer \
    --image us.icr.io/${SN_ICR_NAMESPACE}/senti_analyzer \
    --registry-secret icr-secret \
    --port 5000
```

**Expected Output:**

```
Creating application 'sentianalyzer'...
OK
Run 'ibmcloud ce application get -n sentianalyzer' to see more details.
```

**If this fails:**

*   Check if application already exists: `ibmcloud ce application list`
*   If exists, delete it first: `ibmcloud ce application delete --name sentianalyzer`
*   Verify you're in correct Code Engine project: `ibmcloud ce project current`

### Step 5: Get Application URL

```bash
ibmcloud ce application get --name sentianalyzer
```

**Look for the URL in the output:**

```
URL: https://sentianalyzer.xxxxx.us-south.codeengine.appdomain.cloud
```

**Copy this URL - you'll need it for the next steps!**

### Step 6: Test Welcome Endpoint

```bash
curl https://[YOUR_URL]/
```

**Expected Response:**

```
Welcome to the Sentiment Analyzer. Use /analyze/text to get the sentiment
```

### Step 7: Test Sentiment Analysis

```bash
curl https://[YOUR_URL]/analyze/Fantastic%20services
```

**Expected Response:**

```json
{"sentiment": "positive"}
```

### Step 8: Open in Browser for Screenshot

1.  Open your web browser
2.  Navigate to: `https://[YOUR_URL]/analyze/Fantastic%20services`
3.  You should see: `{"sentiment": "positive"}`
4.  Take a screenshot showing:
    *   The full URL in the address bar
    *   The JSON response
5.  Save as `sentiment_analyzer.png` or `sentiment_analyzer.jpeg`

### Step 9: Update .env File

**Option A: Automatic (if scripts work)**

```bash
cd /Users/Salama/IBM/xrwvm-fullstack_developer_capstone/server/djangoapp/microservices
./update_env.sh
```

**Option B: Manual**

1.  Open file: `/Users/Salama/IBM/xrwvm-fullstack_developer_capstone/server/djangoapp/.env`
2.  Add or update this line:
    ```
    sentiment_analyzer_url=https://[YOUR_URL]/
    ```
    **IMPORTANT: Include the trailing slash `/`**
3.  Save the file

### Step 10: Verify Integration from Django

```bash
cd /Users/Salama/IBM/xrwvm-fullstack_developer_capstone/server
python3 manage.py shell
```

Then in the Python shell:

```python
from djangoapp.restapis import analyze_review_sentiments

# Test positive sentiment
result = analyze_review_sentiments("This is amazing")
print(result)  # Should print: {'sentiment': 'positive'}

# Test negative sentiment
result = analyze_review_sentiments("This is terrible")
print(result)  # Should print: {'sentiment': 'negative'}

# Exit shell
exit()
```

---

## Troubleshooting

### Docker Command Not Found

```bash
# Check if Docker Desktop is running
# Add Docker to PATH (if needed)
export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH"
```

### IBM Cloud Not Logged In

```bash
ibmcloud login
# Follow the prompts to log in
```

### Container Registry Login

```bash
ibmcloud cr login
```

### Check Code Engine Project

```bash
ibmcloud ce project list
ibmcloud ce project select --name [your-project-name]
```

### Application Already Exists

```bash
ibmcloud ce application delete --name sentianalyzer
# Then retry the create command
```

### View Application Logs

```bash
ibmcloud ce application logs --name sentianalyzer --follow
```

---

## Quick Copy-Paste Version

If all prerequisites are met, copy and paste these commands one by one:

```bash
# Navigate to directory
cd /Users/Salama/IBM/xrwvm-fullstack_developer_capstone/server/djangoapp/microservices

# Build Docker image
docker build . -t us.icr.io/${SN_ICR_NAMESPACE}/senti_analyzer

# Push to registry
docker push us.icr.io/${SN_ICR_NAMESPACE}/senti_analyzer

# Deploy to Code Engine
ibmcloud ce application create --name sentianalyzer \
    --image us.icr.io/${SN_ICR_NAMESPACE}/senti_analyzer \
    --registry-secret icr-secret \
    --port 5000

# Get URL
ibmcloud ce application get --name sentianalyzer

# Test (replace [YOUR_URL] with actual URL)
curl [YOUR_URL]/analyze/Fantastic%20services
```

---

## Completion Checklist

- [ ] Docker image built successfully
- [ ] Image pushed to IBM Container Registry
- [ ] Application deployed to Code Engine
- [ ] Application URL obtained
- [ ] Welcome endpoint tested
- [ ] Sentiment analysis endpoint tested
- [ ] Browser test completed
- [ ] Screenshot taken and saved
- [ ] .env file updated with URL (with trailing slash!)
- [ ] Django integration tested and working

---

## Your Deployment URL

Write your deployment URL here for reference:
```
https://_______________________________________________
```

---

## Next Steps After Deployment

1. The sentiment analyzer is now live and accessible
2. Your Django application can call it using `analyze_review_sentiments()`
3. You can integrate it into your review submission workflow
4. Monitor the application: `ibmcloud ce application get --name sentianalyzer`
5. View logs if needed: `ibmcloud ce application logs --name sentianalyzer`

---

**Need Help?** Refer to:
- DEPLOYMENT_GUIDE.md for detailed explanations
- QUICK_DEPLOY.md for quick reference
- VISUAL_GUIDE.md for visual walkthrough
- DEPLOYMENT_CHECKLIST.md for progress tracking
