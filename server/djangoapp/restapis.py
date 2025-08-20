import os
import json
import requests
from dotenv import load_dotenv
from .models import CarDealer, DealerReview
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import (
    Features,
    SentimentOptions,
)
from django.conf import settings
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

load_dotenv()

backend_url = os.getenv(
    'backend_url',
    default=(
        "https://lukaslondono-3030.theiadockernext-0-labs-prod-theiak8s-4-tor01."
        "proxy.cognitiveclass.ai/"
    )
)
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/"
)


def get_request(url, **kwargs):
    """
    Make a GET request to the specified URL.
    Returns the JSON response if successful, None otherwise.
    """
    try:
        response = requests.get(
            url,
            headers={"Content-Type": "application/json"},
            **kwargs
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error making GET request to {url}: {e}")
        return None


def post_request(url, json_payload, **kwargs):
    print(kwargs)
    print("POST to {} ".format(url))
    print(json_payload)
    response = requests.post(url, params=kwargs, json=json_payload)
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


def get_dealers_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url)
    if json_result:
        dealers = json_result["rows"]
        for dealer in dealers:
            dealer_doc = dealer["doc"]
            dealer_obj = CarDealer(
                address=dealer_doc["address"],
                city=dealer_doc["city"],
                full_name=dealer_doc["full_name"],
                id=dealer_doc["id"],
                lat=dealer_doc["lat"],
                long=dealer_doc["long"],
                short_name=dealer_doc["short_name"],
                st=dealer_doc["st"],
                zip=dealer_doc["zip"]
            )
            results.append(dealer_obj)
    return results


def get_dealer_by_id_from_cf(url, dealer_id):
    json_result = get_request(url, dealerId=dealer_id)
    if json_result:
        dealers = json_result["rows"]
        dealer_doc = dealers[0]["doc"]
        dealer_obj = CarDealer(
            address=dealer_doc["address"],
            city=dealer_doc["city"],
            full_name=dealer_doc["full_name"],
            id=dealer_doc["id"],
            lat=dealer_doc["lat"],
            long=dealer_doc["long"],
            short_name=dealer_doc["short_name"],
            st=dealer_doc["st"],
            zip=dealer_doc["zip"]
        )
        return dealer_obj
    return None


def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    json_result = get_request(url, dealerId=dealer_id)
    if json_result:
        reviews = json_result["rows"]
        for review in reviews:
            review_doc = review["doc"]
            review_obj = DealerReview(
                dealership=review_doc["dealership"],
                name=review_doc["name"],
                purchase=review_doc["purchase"],
                review=review_doc["review"],
                purchase_date=review_doc["purchase_date"],
                car_make=review_doc["car_make"],
                car_model=review_doc["car_model"],
                car_year=review_doc["car_year"],
                sentiment=analyze_review_sentiments(review_doc["review"])
            )
            results.append(review_obj)
    return results


def analyze_review_sentiments(text):
    url = (
        "https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/"
        "instances/8c2c3c3c-3c3c-3c3c-3c3c-3c3c3c3c3c3c"
    )
    api_key = "your-api-key"
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2021-08-01',
        authenticator=authenticator
    )
    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze(
        text=text,
        features=Features(sentiment=SentimentOptions(targets=[text]))
    ).get_result()
    label = response['sentiment']['document']['label']
    return label


def post_review(data):
    """
    Post a review to the backend service.
    Returns True if successful, False otherwise.
    """
    url = f"{settings.BACKEND_URL}/postreview"
    try:
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            json=data,
        )
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"Error posting review to {url}: {e}")
        return False
