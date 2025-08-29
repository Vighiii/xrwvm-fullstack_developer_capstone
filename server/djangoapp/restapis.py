import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Backend service and sentiment analyzer URLs from .env
backend_url = os.getenv('backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv('sentiment_analyzer_url', default="http://localhost:5050/")

def get_request(endpoint, **kwargs):
    """
    Send a GET request to the backend service with optional query parameters.
    """
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params += f"{key}={value}&"
    request_url = backend_url + endpoint + "?" + params
    print(f"GET from {request_url}")
    try:
        response = requests.get(request_url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Network exception occurred: {e}")
        return None

def analyze_review_sentiments(text):
    """
    Analyze the sentiment of the given text using the deployed microservice.
    """
    try:
        url = sentiment_analyzer_url + "analyze/" + text
        print(f"GET from {url}")
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get("label", "neutral")
    except requests.RequestException as e:
        print(f"Sentiment analysis failed: {e}")
        return "neutral"

def post_review(data_dict):
    """
    Send a POST request to the backend to submit a review.
    """
    try:
        request_url = backend_url + "/insert_review"
        print(f"POST to {request_url} with data {data_dict}")
        response = requests.post(request_url, json=data_dict)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Failed to post review: {e}")
        return {"error": str(e)}
