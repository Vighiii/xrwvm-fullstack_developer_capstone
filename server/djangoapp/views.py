from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import logging
import json
from .models import CarMake, CarModel
from . import restapis


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"status": True, "userName": user.username})
        else:

            try:
                u = User.objects.get(username=username)
                if not u.check_password(password):
                    return JsonResponse({"status": False, "error": "Wrong password"})
            except User.DoesNotExist:
                return JsonResponse({"status": False, "error": "User not found"})

            return JsonResponse({"status": False, "error": "Authentication failed"})

# Create a `logout_request` view to handle sign out request
@csrf_exempt
def logout_user(request):
    logout(request)
    return JsonResponse({"userName": ""})

# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    context = {}
    # Load JSON data from the request body
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    username_exist = False
    email_exist = False
    try:
        # Check if user already exists
        User.objects.get(username=username)
        username_exist = True
    except:
        # If not, simply log this is a new user
        logger.debug("{} is new user".format(username))
    # If it is a new user
    if not username_exist:
        # Create user in auth_user table
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,password=password, email=email)
        # Login the user and redirect to list page
        login(request, user)
        data = {"userName":username,"status":"Authenticated"}
        return JsonResponse(data)
    else :
        data = {"userName":username,"error":"Already Registered"}
        return JsonResponse(data)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request, state="All"):
    if request.method == "GET":
        endpoint = "/fetchDealers" if state == "All" else "/fetchDealers/" + state
        dealerships = restapis.get_request(endpoint)
        return JsonResponse({"status": 200, "dealers": dealerships})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})

# Create a `get_dealer_reviews` view to render the reviews of a dealer
def get_dealer_reviews(request, dealer_id):
    if request.method == "GET":
        endpoint = "/fetchReviews/dealer/" + str(dealer_id)
        reviews = restapis.get_request(endpoint)
        for review_detail in reviews:
            response = restapis.analyze_review_sentiments(review_detail['review'])
            print(response)
            review_detail['sentiment'] = response['sentiment']
        return JsonResponse({"status": 200, "reviews": reviews})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})

# Create a `get_dealer_details` view to render the dealer details
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        endpoint = "/fetchDealer/" + str(dealer_id)
        dealership = restapis.get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})

# Create a `add_review` view to submit a review
@csrf_exempt
def add_review(request):
    if not request.user.is_anonymous:
        data = json.loads(request.body)
        try:
            restapis.post_review(data)
            return JsonResponse({"status": 200})
        except:
            return JsonResponse({"status": 401, "message": "Error in posting review"})
    else:
        return JsonResponse({"status": 403, "message": "Unauthorized"})

# View to get cars
def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)
    if count == 0:
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
    return JsonResponse({"CarModels": cars})

# Initialize database with sample data
def initiate(request=None):
    # Add sample car makes
    car_make_data = [
        {"name": "Toyota", "description": "Japanese automotive manufacturer"},
        {"name": "Honda", "description": "Japanese public multinational conglomerate"},
        {"name": "Ford", "description": "American multinational automaker"},
        {"name": "Tesla", "description": "American electric vehicle manufacturer"},
        {"name": "BMW", "description": "German multinational manufacturer of luxury vehicles"},
    ]
    
    for item in car_make_data:
        CarMake.objects.create(name=item['name'], description=item['description'])
    
    # Add sample car models
    car_model_data = [
        {"make": "Toyota", "name": "Camry", "type": "SEDAN", "year": 2023},
        {"make": "Toyota", "name": "RAV4", "type": "SUV", "year": 2023},
        {"make": "Honda", "name": "Accord", "type": "SEDAN", "year": 2023},
        {"make": "Honda", "name": "CR-V", "type": "SUV", "year": 2022},
        {"make": "Ford", "name": "F-150", "type": "PICKUP", "year": 2023},
        {"make": "Ford", "name": "Mustang", "type": "COUPE", "year": 2023},
        {"make": "Tesla", "name": "Model 3", "type": "SEDAN", "year": 2023},
        {"make": "Tesla", "name": "Model Y", "type": "SUV", "year": 2023},
        {"make": "BMW", "name": "3 Series", "type": "SEDAN", "year": 2023},
        {"make": "BMW", "name": "X5", "type": "SUV", "year": 2022},
    ]
    
    for item in car_model_data:
        car_make = CarMake.objects.get(name=item['make'])
        CarModel.objects.create(
            car_make=car_make,
            name=item['name'],
            type=item['type'],
            year=item['year']
        )
    
    if request:
        return JsonResponse({"status": "success", "message": "Database initialized"})
