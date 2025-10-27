# Quick Deployment Reference

## One-Line Commands (Copy & Paste)

### 1. Navigate to Directory

```bash
cd server/djangoapp/microservices
```

### 2. Build Docker Image

```bash
docker build . -t us.icr.io/${SN_ICR_NAMESPACE}/senti_analyzer
```

### 3. Push to Registry

```bash
docker push us.icr.io/${SN_ICR_NAMESPACE}/senti_analyzer
```

### 4. Deploy to Code Engine

```bash
ibmcloud ce application create --name sentianalyzer --image us.icr.io/${SN_ICR_NAMESPACE}/senti_analyzer --registry-secret icr-secret --port 5000
```

### 5. Get Application URL

```bash
ibmcloud ce application get --name sentianalyzer | grep URL
```

### 6. Test Deployment

```bash
# Replace YOUR_URL with the actual URL from step 5
curl YOUR_URL/analyze/Fantastic%20services
```

### 7. Update .env File

```bash
# Replace YOUR_URL with the actual URL (include trailing slash!)
echo "sentiment_analyzer_url=YOUR_URL/" >> ../.env
```

## Expected Output Examples

### After Build

```
Successfully built abc123def456
Successfully tagged us.icr.io/your-namespace/senti_analyzer:latest
```

### After Push

```
The push refers to repository [us.icr.io/your-namespace/senti_analyzer]
latest: digest: sha256:abc123... size: 1234
```

### After Deploy

```
Creating application 'sentianalyzer'...
OK
Run 'ibmcloud ce application get -n sentianalyzer' to see more details.
```

### Application URL

```
https://sentianalyzer.xxxxxxxxx.us-south.codeengine.appdomain.cloud
```

### Test Response

```json
{"sentiment": "positive"}
```

## Automated Script

For automated deployment, use:

```bash
chmod +x deploy.sh
./deploy.sh
```

## Verification Checklist

- [ ] Docker image built successfully
- [ ] Docker image pushed to registry
- [ ] Code Engine application created
- [ ] Application URL obtained
- [ ] Welcome endpoint responds (/)
- [ ] Sentiment endpoint works (/analyze/Fantastic%20services)
- [ ] Screenshot taken with URL visible
- [ ] .env file updated with URL (with trailing slash!)
- [ ] Django app can call the microservice

## Common Issues & Quick Fixes

| Issue | Quick Fix |
|-------|-----------|
| `SN_ICR_NAMESPACE not set` | `export SN_ICR_NAMESPACE=your-namespace` |
| `Docker daemon not running` | Start Docker Desktop |
| `Not logged into IBM Cloud` | `ibmcloud login` |
| `Application already exists` | `ibmcloud ce application delete --name sentianalyzer` then retry |
| `Port 5000 not accessible` | Check firewall settings |

## Important Notes

⚠️ **Always include the trailing slash** in the .env file:
```
✅ sentiment_analyzer_url=https://your-url/
❌ sentiment_analyzer_url=https://your-url
```

⚠️ **Test before updating .env:**
```bash
curl https://your-url/analyze/test
```

⚠️ **Screenshot must show:**
- Full URL in browser address bar
- JSON response with sentiment
- Save as sentiment_analyzer.png or sentiment_analyzer.jpeg
