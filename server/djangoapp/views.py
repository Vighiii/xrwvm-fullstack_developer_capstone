# Uncomment the required imports before adding the code

# from django.shortcuts import render
# from django.http import HttpResponseRedirect, HttpResponse
# from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404, render, redirect
# from django.contrib.auth import logout
# from django.contrib import messages
# from datetime import datetime

from .models import CarMake, CarModel
from .populate import initiate
from .restapis import get_request, analyze_review_sentiments, post_review
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
import logging
import json
from django.views.decorators.csrf import csrf_exempt
# from .populate import initiate


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']

    user = authenticate(username=username, password=password)

    data = {"userName": username}

    if user is not None:
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}

    return JsonResponse(data)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return JsonResponse({"userName": ""})


# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    if request.method == "POST":
        data = json.loads(request.body)

        username = data.get("userName")
        password = data.get("password")
        first_name = data.get("firstName")
        last_name = data.get("lastName")
        email = data.get("email")

        if not username or not password:
            return JsonResponse(
                {"error": "Username and password are required"},
                status=400
            )

        if User.objects.filter(username=username).exists():
            return JsonResponse(
                {"error": "Username already exists"},
                status=400
            )

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        return JsonResponse(
            {"userName": user.username, "status": "Registered"},
            status=201
        )

    return JsonResponse(
        {"error": "POST request required"},
        status=405
    )
def get_cars(request):
    if CarMake.objects.count() == 0:
        initiate()

    car_models = CarModel.objects.select_related('car_make')

    cars = []

    for car_model in car_models:
        cars.append({
            "CarModel": car_model.name,
            "CarMake": car_model.car_make.name
        })

    return JsonResponse({"CarModels": cars})

# Get all dealerships
def get_dealerships(request):
    return JsonResponse(
        get_request("/fetchDealers"),
        safe=False
    )


# Get dealership details by ID
def get_dealer_details(request, dealer_id):
    return JsonResponse(
        get_request(f"/fetchDealer/{dealer_id}"),
        safe=False
    )


# Get dealerships by state
def get_dealerships_by_state(request, state):
    return JsonResponse(
        get_request(f"/fetchDealers/{state}"),
        safe=False
    )


# Get reviews for a particular dealer
def get_dealer_reviews(request, dealer_id):
    return JsonResponse(
        get_request(f"/fetchReviews/dealer/{dealer_id}"),
        safe=False
    )


# Analyze sentiment of a review
def analyze_review(request, text):
    return JsonResponse(
        analyze_review_sentiments(text)
    )


# Add a review
@csrf_exempt
def add_review(request):
    if request.method == "POST":
        data = json.loads(request.body)
        result = post_review(data)
        return JsonResponse(result)

    return JsonResponse(
        {"error": "POST request required"},
        status=405
    )
