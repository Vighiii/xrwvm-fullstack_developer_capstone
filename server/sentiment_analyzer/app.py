from __future__ import annotations

import os
from pathlib import Path

from flask import Flask, jsonify

try:
    from nltk.sentiment import SentimentIntensityAnalyzer
except ImportError:  # pragma: no cover
    SentimentIntensityAnalyzer = None

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent


def build_analyzer():
    if SentimentIntensityAnalyzer is None:
        return None
    lexicon = BASE_DIR / "vader_lexicon.txt"
    candidates = [
        f"file:{lexicon.as_posix()}",
        str(lexicon),
    ]
    for candidate in candidates:
        try:
            return SentimentIntensityAnalyzer(lexicon_file=candidate)
        except (LookupError, OSError, ValueError):
            continue
    try:
        return SentimentIntensityAnalyzer()
    except LookupError:
        return None


sia = build_analyzer()


def fallback_sentiment(text: str) -> str:
    positive = {
        "amazing", "awesome", "best", "excellent", "fantastic", "friendly",
        "good", "great", "happy", "helpful", "love", "perfect", "professional",
        "quick", "recommend", "satisfied", "service", "services", "wonderful",
    }
    negative = {
        "angry", "awful", "bad", "broken", "disappointed", "hate", "horrible",
        "poor", "rude", "slow", "terrible", "unhappy", "worst",
    }
    words = {word.strip(".,!?;:\"'()[]{}").lower() for word in text.split()}
    positive_score = len(words & positive)
    negative_score = len(words & negative)
    if positive_score > negative_score:
        return "positive"
    if negative_score > positive_score:
        return "negative"
    return "neutral"


def analyze(text: str) -> str:
    if sia is None:
        return fallback_sentiment(text)
    scores = sia.polarity_scores(text)
    compound = float(scores.get("compound", 0.0))
    if compound >= 0.05:
        return "positive"
    if compound <= -0.05:
        return "negative"
    return "neutral"


@app.get("/")
def home():
    return jsonify(
        {
            "message": "Welcome to the Best Cars Sentiment Analyzer",
            "usage": "/analyze/<review text>",
        }
    )


@app.get("/health")
def health():
    return jsonify({"status": "ok", "vader_loaded": sia is not None})


@app.get("/analyze/<path:input_txt>")
def analyze_sentiment(input_txt: str):
    return jsonify({"sentiment": analyze(input_txt)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5050")), debug=False)
