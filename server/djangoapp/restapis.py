import os
import requests
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv(
    'backend_url', default='http://localhost:3030'
)
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default='http://localhost:5050/'
)


def get_request(endpoint, **kwargs):
    """Make a GET request to the backend service."""
    params = ''
    if kwargs:
        for key, value in kwargs.items():
            params = f'{params}{key}={value}&'

    request_url = f'{backend_url}{endpoint}?{params}'
    print(f'GET from {request_url}')

    try:
        response = requests.get(request_url)
        response.raise_for_status()
        return response.json() or []
    except Exception as e:
        print(f'Network exception occurred: {e}')
        return []


def analyze_review_sentiments(text):
    """Call the sentiment analyzer service."""
    request_url = f'{sentiment_analyzer_url}analyze/{text}'
    print(f'GET from {request_url}')

    try:
        response = requests.get(request_url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f'Unexpected error: {e}')
        return {'sentiment': 'neutral'}


def post_review(data_dict):
    request_url = backend_url+"/insert_review"
    try:
        response = requests.post(request_url,json=data_dict)
        print(response.json())
        return response.json()
    except:
        print("Network exception occurred")
