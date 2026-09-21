import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv(
    'backend_url',
    default="http://localhost:3030"
)

sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/"
)


def get_request(endpoint, **kwargs):
    request_url = backend_url + endpoint
    response = requests.get(request_url, **kwargs)
    return response.json()


def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url + "analyze/" + text
    response = requests.get(request_url)
    return response.json()


def post_review(data_dict):
    request_url = backend_url + "/insert_review"

    response = requests.post(
        request_url,
        data=json.dumps(data_dict),
        headers={"Content-Type": "application/json"}
    )

    return response.json()
