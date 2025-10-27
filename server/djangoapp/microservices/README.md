# Sentiment Analyzer Microservice

A Flask-based microservice that performs sentiment analysis using NLTK's VADER (Valence Aware Dictionary and sEntiment Reasoner) sentiment analyzer.

## Overview

This microservice provides REST API endpoints to analyze the sentiment of text input and returns whether the sentiment is positive, negative, or neutral.

## Features

- **Real-time Sentiment Analysis**: Analyzes text and returns sentiment scores
- **Simple REST API**: Easy-to-use HTTP endpoints
- **NLTK VADER**: Uses industry-standard sentiment analysis
- **Containerized**: Ready for deployment with Docker
- **Cloud-Ready**: Optimized for IBM Code Engine deployment

## API Endpoints

### 1. Welcome Endpoint

```
GET /
```

Returns a welcome message with usage instructions.

**Response:**

```
Welcome to the Sentiment Analyzer. Use /analyze/text to get the sentiment
```

### 2. Analyze Sentiment

```
GET /analyze/<text>
```

Analyzes the sentiment of the provided text.

**Parameters:**

- `text` (string): The text to analyze (URL encoded)

**Response:**

```json
{
  "sentiment": "positive" | "negative" | "neutral"
}
```

**Examples:**

```bash
# Positive sentiment
curl https://your-url/analyze/I%20love%20this%20product
# Response: {"sentiment": "positive"}

# Negative sentiment
curl https://your-url/analyze/This%20is%20terrible
# Response: {"sentiment": "negative"}

# Neutral sentiment
curl https://your-url/analyze/It%20is%20okay
# Response: {"sentiment": "neutral"}
```

## Project Structure

```
microservices/
├── app.py                      # Flask application with sentiment analysis
├── Dockerfile                  # Docker configuration
├── requirements.txt            # Python dependencies
├── sentiment/                  # NLTK sentiment data
│   ├── readme.md
│   └── vader_lexicon.zip
├── deploy.sh                   # Automated deployment script
├── update_env.sh              # Script to update .env file
├── test_deployment.sh         # Deployment testing script
├── DEPLOYMENT_GUIDE.md        # Detailed deployment instructions
├── QUICK_DEPLOY.md            # Quick reference commands
└── README.md                  # This file
```

## Local Development

### Prerequisites

- Python 3.9+
- pip
- Virtual environment (recommended)

### Setup

1. **Create virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Download NLTK data:**

   ```python
   python3 -c "import nltk; nltk.download('vader_lexicon')"
   ```

4. **Run the application:**

   ```bash
   python3 app.py
   ```

   Or:

   ```bash
   flask run --host=0.0.0.0 --port=5000
   ```

5. **Test locally:**

   ```bash
   curl http://localhost:5000/
   curl http://localhost:5000/analyze/This%20is%20great
   ```

## Docker Deployment

### Build Image

```bash
docker build -t senti_analyzer .
```

### Run Container

```bash
docker run -p 5000:5000 senti_analyzer
```

### Test Container

```bash
curl http://localhost:5000/analyze/Amazing%20service
```

## IBM Code Engine Deployment

### Quick Deploy (Automated)

1. **Make scripts executable:**

   ```bash
   chmod +x deploy.sh update_env.sh test_deployment.sh
   ```

2. **Run deployment:**

   ```bash
   ./deploy.sh
   ```

3. **Update .env file:**

   ```bash
   ./update_env.sh
   ```

4. **Test deployment:**

   ```bash
   ./test_deployment.sh
   ```

### Manual Deploy

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.

### Quick Reference

See [QUICK_DEPLOY.md](QUICK_DEPLOY.md) for copy-paste commands.

## Integration with Django

The microservice is integrated with the Django application through `restapis.py`:

```python
from djangoapp.restapis import analyze_review_sentiments

# Analyze sentiment
result = analyze_review_sentiments("This product is amazing")
print(result)  # {'sentiment': 'positive'}
```

### Configuration

Add to `server/djangoapp/.env`:

```
sentiment_analyzer_url=https://your-code-engine-url/
```

**Important:** Include the trailing slash `/`

## How It Works

1. **Input**: Text is received via HTTP GET request
2. **Processing**: NLTK's VADER analyzer calculates sentiment scores:
   - `pos`: Positive score (0-1)
   - `neg`: Negative score (0-1)
   - `neu`: Neutral score (0-1)
   - `compound`: Overall sentiment (-1 to 1)
3. **Classification**: Determines sentiment based on highest score:
   - If `neg` is highest → "negative"
   - If `neu` is highest → "neutral"
   - Otherwise → "positive"
4. **Output**: Returns JSON with sentiment classification

## Sentiment Analysis Algorithm

The service uses NLTK's VADER (Valence Aware Dictionary and sEntiment Reasoner):

- **Lexicon-based**: Uses a pre-built dictionary of sentiment-scored words
- **Context-aware**: Considers punctuation, capitalization, and modifiers
- **Social media optimized**: Works well with informal text
- **No training required**: Ready to use out of the box

## Testing

### Unit Tests

```bash
# Test welcome endpoint
curl https://your-url/

# Test positive sentiment
curl https://your-url/analyze/Fantastic%20services

# Test negative sentiment
curl https://your-url/analyze/Terrible%20experience

# Test neutral sentiment
curl https://your-url/analyze/It%20is%20okay
```

### Automated Testing

```bash
./test_deployment.sh
```

## Troubleshooting

### Common Issues

1. **NLTK data not found**

   ```bash
   python3 -c "import nltk; nltk.download('vader_lexicon')"
   ```

2. **Port already in use**

   ```bash
   # Change port in Dockerfile or use different port
   flask run --port=5001
   ```

3. **Docker build fails**

   ```bash
   # Clear Docker cache
   docker system prune -a
   docker build --no-cache -t senti_analyzer .
   ```

4. **Code Engine deployment fails**

   ```bash
   # Check application status
   ibmcloud ce application get --name sentianalyzer
   
   # View logs
   ibmcloud ce application logs --name sentianalyzer
   ```

## Performance

- **Response Time**: < 100ms for typical requests
- **Scalability**: Auto-scales on Code Engine based on load
- **Availability**: High availability with Code Engine's built-in redundancy

## Security

- **No authentication required**: Public endpoint (add auth if needed)
- **Input validation**: Text is URL-encoded
- **No data storage**: Stateless service, no data persistence
- **HTTPS**: Encrypted communication on Code Engine

## Monitoring

### Check Application Status

```bash
ibmcloud ce application get --name sentianalyzer
```

### View Logs

```bash
ibmcloud ce application logs --name sentianalyzer --follow
```

### Metrics

```bash
ibmcloud ce application events --name sentianalyzer
```

## Maintenance

### Update Deployment

```bash
# Rebuild and push new image
docker build -t us.icr.io/${SN_ICR_NAMESPACE}/senti_analyzer .
docker push us.icr.io/${SN_ICR_NAMESPACE}/senti_analyzer

# Update Code Engine application
ibmcloud ce application update --name sentianalyzer \
    --image us.icr.io/${SN_ICR_NAMESPACE}/senti_analyzer
```

### Delete Deployment

```bash
ibmcloud ce application delete --name sentianalyzer
```

## Dependencies

- **Flask**: Web framework
- **NLTK**: Natural Language Toolkit for sentiment analysis
- **Python 3.9**: Runtime environment

See [requirements.txt](requirements.txt) for specific versions.

## License

This project is part of the IBM Full Stack Developer Capstone.

## Support

For issues or questions:

1. Check [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
2. Review [QUICK_DEPLOY.md](QUICK_DEPLOY.md)
3. Check IBM Code Engine documentation
4. Review application logs

## Contributing

To improve the sentiment analyzer:

1. Modify `app.py` with your changes
2. Test locally
3. Rebuild Docker image
4. Redeploy to Code Engine
5. Update tests

## Future Enhancements

Potential improvements:

- [ ] Add authentication/API keys
- [ ] Support batch analysis
- [ ] Add more sentiment categories (very positive, very negative)
- [ ] Include confidence scores in response
- [ ] Add support for multiple languages
- [ ] Implement caching for common phrases
- [ ] Add rate limiting
- [ ] Provide detailed sentiment breakdown
