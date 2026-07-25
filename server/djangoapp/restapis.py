"""HTTP helpers for the Node backend and sentiment service.

The module includes a local JSON fallback so the Django deployment remains usable
when the optional Node/Mongo or sentiment containers are unavailable.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any
from urllib.parse import quote

import requests
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

backend_url = os.getenv("backend_url", "http://localhost:3030").rstrip("/")
sentiment_analyzer_url = os.getenv(
    "sentiment_analyzer_url", "http://localhost:5050"
).rstrip("/")

DATA_DIR = BASE_DIR / "database" / "data"


def _load_json(filename: str, key: str) -> list[dict[str, Any]]:
    path = DATA_DIR / filename
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return list(payload.get(key, []))


FALLBACK_DEALERS = _load_json("dealerships.json", "dealerships")
FALLBACK_REVIEWS = _load_json("reviews.json", "reviews")


def _fallback_get(endpoint: str) -> Any:
    endpoint = endpoint.strip("/")

    if endpoint == "fetchDealers":
        return FALLBACK_DEALERS

    if endpoint.startswith("fetchDealers/"):
        state = endpoint.split("/", 1)[1].lower()
        if state == "all":
            return FALLBACK_DEALERS
        return [
            dealer
            for dealer in FALLBACK_DEALERS
            if str(dealer.get("state", "")).lower() == state
            or str(dealer.get("st", "")).lower() == state
        ]

    if endpoint.startswith("fetchDealer/"):
        dealer_id = int(endpoint.rsplit("/", 1)[1])
        return [dealer for dealer in FALLBACK_DEALERS if dealer.get("id") == dealer_id]

    if endpoint == "fetchReviews":
        return FALLBACK_REVIEWS

    if endpoint.startswith("fetchReviews/dealer/"):
        dealer_id = int(endpoint.rsplit("/", 1)[1])
        return [
            review
            for review in FALLBACK_REVIEWS
            if int(review.get("dealership", 0)) == dealer_id
        ]

    return None


def get_request(endpoint: str, **kwargs: Any) -> Any:
    request_url = f"{backend_url}/{endpoint.lstrip('/')}"
    try:
        response = requests.get(request_url, params=kwargs or None, timeout=5)
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError, TypeError):
        return _fallback_get(endpoint)


def _simple_sentiment(text: str) -> str:
    positive = {
        "amazing", "awesome", "best", "excellent", "fantastic", "good",
        "great", "happy", "helpful", "love", "perfect", "professional",
        "quick", "recommend", "satisfied", "service", "services", "wonderful",
    }
    negative = {
        "angry", "awful", "bad", "broken", "disappointed", "hate", "horrible",
        "poor", "rude", "slow", "terrible", "unhappy", "worst",
    }
    words = {word.strip(".,!?;:\"'()[]{}").lower() for word in text.split()}
    pos_score = len(words & positive)
    neg_score = len(words & negative)
    if pos_score > neg_score:
        return "positive"
    if neg_score > pos_score:
        return "negative"
    return "neutral"


def analyze_review_sentiments(text: str) -> dict[str, str]:
    request_url = f"{sentiment_analyzer_url}/analyze/{quote(text, safe='')}"
    try:
        response = requests.get(request_url, timeout=5)
        response.raise_for_status()
        data = response.json()
        sentiment = str(data.get("sentiment", "neutral")).lower()
        if sentiment not in {"positive", "negative", "neutral"}:
            sentiment = "neutral"
        return {"sentiment": sentiment}
    except (requests.RequestException, ValueError, TypeError):
        return {"sentiment": _simple_sentiment(text)}


def post_review(data_dict: dict[str, Any]) -> Any:
    request_url = f"{backend_url}/insert_review"
    try:
        response = requests.post(request_url, json=data_dict, timeout=5)
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError, TypeError):
        existing_ids = [int(item.get("id", 0)) for item in FALLBACK_REVIEWS]
        review = dict(data_dict)
        review["id"] = max(existing_ids, default=0) + 1
        FALLBACK_REVIEWS.append(review)
        return review
