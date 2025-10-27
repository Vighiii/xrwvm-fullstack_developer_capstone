# Sentiment Analyzer Deployment Checklist

Use this checklist to track your deployment progress.

## Pre-Deployment Setup

### Environment Setup

*   \[ ] IBM Cloud CLI installed
    ```bash
    # Verify: ibmcloud --version
    ```
*   \[ ] Docker installed and running
    ```bash
    # Verify: docker --version
    # Check: docker ps
    ```
*   \[ ] Logged into IBM Cloud
    ```bash
    ibmcloud login
    ```
*   \[ ] Code Engine plugin installed
    ```bash
    ibmcloud plugin install code-engine
    # Verify: ibmcloud plugin list
    ```
*   \[ ] Environment variable set
    ```bash
    echo $SN_ICR_NAMESPACE
    # Should display your namespace
    ```

### File Verification

*   \[ ] `app.py` exists and contains Flask application
*   \[ ] `Dockerfile` exists and is properly configured
*   \[ ] `requirements.txt` contains Flask and nltk
*   \[ ] `sentiment/vader_lexicon.zip` exists
*   \[ ] Deployment scripts are executable
    ```bash
    chmod +x deploy.sh update_env.sh test_deployment.sh
    ```

## Deployment Process

### Step 1: Navigate to Directory

*   \[ ] Changed to microservices directory
    ```bash
    cd server/djangoapp/microservices
    pwd  # Should show: .../server/djangoapp/microservices
    ```

### Step 2: Build Docker Image

*   \[ ] Docker build command executed
    ```bash
    docker build . -t us.icr.io/${SN_ICR_NAMESPACE}/senti_analyzer
    ```
*   \[ ] Build completed successfully
*   \[ ] No error messages in output
*   \[ ] Image appears in Docker images list
    ```bash
    docker images | grep senti_analyzer
    ```

**Expected Output:**

```
Successfully built [image-id]
Successfully tagged us.icr.io/[namespace]/senti_analyzer:latest
```

### Step 3: Push Docker Image

*   \[ ] Docker push command executed
    ```bash
    docker push us.icr.io/${SN_ICR_NAMESPACE}/senti_analyzer
    ```
*   \[ ] Push completed successfully
*   \[ ] Image uploaded to IBM Container Registry

**Expected Output:**

```
The push refers to repository [us.icr.io/[namespace]/senti_analyzer]
latest: digest: sha256:[hash] size: [size]
```

### Step 4: Deploy to Code Engine

*   \[ ] Deployment command executed
    ```bash
    ibmcloud ce application create --name sentianalyzer \
        --image us.icr.io/${SN_ICR_NAMESPACE}/senti_analyzer \
        --registry-secret icr-secret \
        --port 5000
    ```
*   \[ ] Application created successfully
*   \[ ] No error messages

**Expected Output:**

```
Creating application 'sentianalyzer'...
OK
```

### Step 5: Get Application URL

*   \[ ] Retrieved application URL
    ```bash
    ibmcloud ce application get --name sentianalyzer
    ```
*   \[ ] URL copied and saved
*   \[ ] URL format verified (https://...)

**Application URL:**

```
_________________________________
(Write your URL here)
```

### Step 6: Test Deployment

#### Test 1: Welcome Endpoint

*   \[ ] Tested welcome endpoint
    ```bash
    curl [YOUR_URL]/
    ```
*   \[ ] Received welcome message

**Expected Response:**

```
Welcome to the Sentiment Analyzer. Use /analyze/text to get the sentiment
```

#### Test 2: Sentiment Analysis - Positive

*   \[ ] Tested with positive text
    ```bash
    curl [YOUR_URL]/analyze/Fantastic%20services
    ```
*   \[ ] Received positive sentiment

**Expected Response:**

```json
{"sentiment": "positive"}
```

#### Test 3: Sentiment Analysis - Negative

*   \[ ] Tested with negative text
    ```bash
    curl [YOUR_URL]/analyze/Terrible%20experience
    ```
*   \[ ] Received negative sentiment

**Expected Response:**

```json
{"sentiment": "negative"}
```

#### Test 4: Browser Test

*   \[ ] Opened URL in browser: `[YOUR_URL]/analyze/Fantastic%20services`
*   \[ ] JSON response displayed correctly
*   \[ ] URL visible in address bar

### Step 7: Screenshot

*   \[ ] Browser opened to: `[YOUR_URL]/analyze/Fantastic%20services`
*   \[ ] Screenshot taken showing:
    *   \[ ] Full URL in address bar
    *   \[ ] JSON response: `{"sentiment": "positive"}`
*   \[ ] Screenshot saved as `sentiment_analyzer.png` or `sentiment_analyzer.jpeg`
*   \[ ] Screenshot file location: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

### Step 8: Update .env File

#### Option A: Automated

*   \[ ] Ran update script
    ```bash
    ./update_env.sh
    ```
*   \[ ] Script completed successfully
*   \[ ] Verified .env file updated

#### Option B: Manual

*   \[ ] Opened `server/djangoapp/.env` file
*   \[ ] Added/updated line:
    ```
    sentiment_analyzer_url=[YOUR_URL]/
    ```
*   \[ ] **Verified trailing slash is included** ⚠️
*   \[ ] Saved file

**Verify .env content:**

```bash
grep sentiment_analyzer_url server/djangoapp/.env
```

**Expected Output:**

```
sentiment_analyzer_url=https://[your-url]/
```

### Step 9: Verify Integration

#### Test from Django Shell

*   \[ ] Started Django shell
    ```bash
    cd ../..  # Back to server directory
    python3 manage.py shell
    ```
*   \[ ] Imported function
    ```python
    from djangoapp.restapis import analyze_review_sentiments
    ```
*   \[ ] Tested function
    ```python
    result = analyze_review_sentiments("This is amazing")
    print(result)
    ```
*   \[ ] Received correct response: `{'sentiment': 'positive'}`

#### Test Different Sentiments

*   \[ ] Positive test
    ```python
    analyze_review_sentiments("Excellent service")
    # Expected: {'sentiment': 'positive'}
    ```
*   \[ ] Negative test
    ```python
    analyze_review_sentiments("Horrible experience")
    # Expected: {'sentiment': 'negative'}
    ```
*   \[ ] Neutral test
    ```python
    analyze_review_sentiments("It is okay")
    # Expected: {'sentiment': 'neutral'} or similar
    ```

## Post-Deployment Verification

### Application Status

*   \[ ] Checked application status
    ```bash
    ibmcloud ce application get --name sentianalyzer
    ```
*   \[ ] Status shows "Ready: true"
*   \[ ] No errors in status

### Application Logs

*   \[ ] Viewed application logs
    ```bash
    ibmcloud ce application logs --name sentianalyzer
    ```
*   \[ ] No error messages in logs
*   \[ ] Application started successfully

### Performance Check

*   \[ ] Response time < 1 second
*   \[ ] Multiple requests handled correctly
*   \[ ] No timeout errors

## Documentation

*   \[ ] Screenshot saved and named correctly
*   \[ ] Deployment URL documented
*   \[ ] .env file updated and verified
*   \[ ] All tests passed and documented

## Cleanup (Optional)

If you need to redeploy or remove:

### Delete Application

*   \[ ] Delete command executed (if needed)
    ```bash
    ibmcloud ce application delete --name sentianalyzer
    ```

### Remove Docker Image

*   \[ ] Local image removed (if needed)
    ```bash
    docker rmi us.icr.io/${SN_ICR_NAMESPACE}/senti_analyzer
    ```

## Troubleshooting Log

If you encountered any issues, document them here:

### Issue 1:

**Problem:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
**Solution:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
**Status:** \[ ] Resolved \[ ] Pending

### Issue 2:

**Problem:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
**Solution:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
**Status:** \[ ] Resolved \[ ] Pending

## Final Verification

*   \[ ] All deployment steps completed
*   \[ ] All tests passed
*   \[ ] Screenshot captured and saved
*   \[ ] .env file updated correctly
*   \[ ] Django integration verified
*   \[ ] Application accessible via URL
*   \[ ] No errors in logs
*   \[ ] Documentation complete

## Deployment Summary

**Deployment Date:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
**Deployment Time:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
**Application URL:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
**Status:** \[ ] Success \[ ] Failed \[ ] Partial

**Notes:**
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

---

## Quick Reference

### Useful Commands

**Check application status:**

```bash
ibmcloud ce application get --name sentianalyzer
```

**View logs:**

```bash
ibmcloud ce application logs --name sentianalyzer --follow
```

**Test endpoint:**

```bash
curl [YOUR_URL]/analyze/test
```

**Update application:**

```bash
ibmcloud ce application update --name sentianalyzer \
    --image us.icr.io/${SN_ICR_NAMESPACE}/senti_analyzer
```

**Restart application:**

```bash
ibmcloud ce application update --name sentianalyzer
```

---

**Checklist Complete:** \[ ] Yes \[ ] No
**Ready for Production:** \[ ] Yes \[ ] No
**Signed Off By:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
**Date:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
