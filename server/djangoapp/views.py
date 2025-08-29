from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
import logging
import json
from .models import CarMake, CarModel
from dotenv import load_dotenv

# REST API and Sentiment Analysis
from .restapis import get_request, post_review, analyze_review_sentiments

# Load environment variables
load_dotenv()

# Logger
logger = logging.getLogger(__name__)

# ============================
# User Authentication
# ============================

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['userName']
        password = data['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({"userName": username, "status": "Authenticated"})
        return JsonResponse({"userName": username, "status": "Failed"})
    return JsonResponse({"status": "Only POST method allowed."}, status=405)


def logout_request(request):
    logout(request)
    return JsonResponse({"userName": ""})


@csrf_exempt
def registration(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data['userName']
            password = data['password']
            first_name = data.get('firstName', '')
            last_name = data.get('lastName', '')
            email = data.get('email', '')

            if User.objects.filter(username=username).exists():
                return JsonResponse({"userName": username, "error": "Already Registered"})

            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            login(request, user)
            return JsonResponse({"userName": username, "status": "Authenticated"})

        except Exception as e:
            logger.error(f"Registration error: {e}")
            return JsonResponse({"error": "Registration failed."}, status=400)
    return JsonResponse({"status": "Only POST method allowed."}, status=405)


# ============================
# Local Car Models
# ============================

def get_cars(request):
    if request.method == 'GET':
        cars = CarModel.objects.all()
        results = []
        for car in cars:
            results.append({
                "id": car.id,
                "name": car.name,
                "type": car.type,
                "year": car.year,
                "dealer_id": car.dealer_id,
                "make": {
                    "id": car.car_make.id,
                    "name": car.car_make.name,
                    "description": car.car_make.description
                }
            })
        return JsonResponse(results, safe=False)
    return JsonResponse({"error": "Only GET method allowed."}, status=405)


# ============================
# Dealer & Reviews API
# ============================

def get_dealerships(request, state="All"):
    endpoint = "/fetchDealers" if state == "All" else f"/fetchDealers/{state}"
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchDealer/{dealer_id}"
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    return JsonResponse({"status": 400, "message": "Bad Request"})


def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail.get('review', ''))
            review_detail['sentiment'] = response.get('sentiment', 'neutral')
        return JsonResponse({"status": 200, "reviews": reviews})
    return JsonResponse({"status": 400, "message": "Bad Request"})


@csrf_exempt
def add_review(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            result = post_review(data)
            return JsonResponse(result)
        except Exception as e:
            logger.error(f"Post review error: {e}")
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Only POST method allowed."}, status=405)
