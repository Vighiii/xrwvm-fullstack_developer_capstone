# Uncomment the required imports before adding the code

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .populate import initiate, initiate_car_models, initiate_car_makes
from .models import CarMake, CarModel
from .restapis import get_request, analyze_review_sentiments, post_review

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    data = {"userName":""}
    return JsonResponse(data)


# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    context = {}
    data = json.loads(request.body.decode('utf-8'))
    print("data: ", data)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    username_exist = False
    email_exist = False

    try:
        # Check if user already exist
        User.objects.get(username=username)
        username_exist=True
    except:
        #If not, simply log this is a new user
        logger.debug("{} is new user".format(username))
    
    # If it is a new user
    if not username_exist:
        # Create user in auth_user table
        user = User.objects.create_user(
            username=username,
            first_name = first_name,
            last_name = last_name,
            password = password,
            email = email,
        )
        # Login the user and redirect to list page
        login(request, user)
        data = {"userName":username, "status":"Authenticated"}
        return JsonResponse(data)
    else:
        data = {"userName":username, "error":"Already Registered"}
        return JsonResponse(data)


# Get the list of the cars
def get_cars(request):
    count = CarMake.objects.filter().count() # standard way in Django to count records in a database table.
    print("count: ", count)
    if (count == 0):
        # Create a list of car makers and car models and save it automatically stored in databased by the create()
        initiate()
    if CarModel.objects.filter().count() == 0:
        initiate_car_models()
        print("Car Model were created.")
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
    return JsonResponse({"CarModels":cars})


# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
def get_dealerships(request, state="All"):
    """
    Fetches dealerships optionally filtered by state.
    """
    try:
        if (state == "All"):
            endpoint = "/fetchDealers"
        else:
            endpoint = "/fetchDealers/"+state
        dealerships = get_request(endpoint)
    except Exception as err:
        print(f"Error fetching dealerships for state {state}: {err}")
        return JsonResponse({"status":500, "message": "Error fetching dealer details."})
    return JsonResponse({"status":200, "dealers":dealerships})


# Create a `get_dealer_details` view to render the dealer details
# Fetches dealer details for a given dealer ID.
def get_dealer_details(request, dealer_id):
    """
    Fetches Dealer details.
    """
    if not dealer_id:
        return JsonResponse({"status": 400,"message": "Bad Request"})
    
    end_point = f"/fetchDealer/{dealer_id}"
    try:
        dealer_details = get_request(end_point)
    except Exception as err:
        print(f"Error getting dealers {dealer_id} with error {err}" )
        return JsonResponse({"status": 500, "message": "Error fetching dealer details"})
    return JsonResponse({"status": 200, "dealer":dealer_details})


# Create a `get_dealer_reviews` view to render the reviews of a dealer
def get_dealer_reviews(request, dealer_id):
    """
    Fetches reviews for a given dealer and analyzes their sentiments.
    """
    if not dealer_id:
        return JsonResponse({"status": 400,"message": "Bad Request"})
    end_point = f"/fetchReviews/dealer/{dealer_id}"
    try:
        get_reviews = get_request(end_point)
        print("get_reviews", get_reviews)
        if not get_reviews:
            print("There are no review for this dealer.")
            return JsonResponse({"status": 200, "message": "No reviews available", "reviews": []})
        else:
            # Convert reviews to string format and analyze sentiments
            for review in get_reviews:
                try: 
                    sentiment = analyze_review_sentiments(review["review"])
                    review["sentiment"] = sentiment
                except Exception as sentiment_err:
                    print(f"Error analyzing sentiment for review: {sentiment_err}.")
                    review["sentiment"] = "error"
    except Exception as err:
        print(f"Error getting review from dealers {dealer_id} with error {err}" )
        return JsonResponse({"status":500, "message": "Error fetching dealer reviews"})
    return JsonResponse({"status":200, "reviews":get_reviews})
 

# Create a `add_review` view to submit a review
def add_review(request):
    """
    Add a new review for a dealers.
    """
    if not request.user.is_authenticated:
        return JsonResponse({"status":403, "message":"Unauthorized"})
    try:
        data = json.loads(request.body)
        response = post_review(data)
        if response.status_code == 201:
            return JsonResponse({"status":201, "message": "Review successfully added"})
        else:
            return JsonResponse({"status": response.status_code, "message": "Could not post a review"})
    except json.JSONDecodeError:
        return JsonResponse({"status": 400, "message": "Invalid JSON format"}, status=400)
    except Exception as err:
        return JsonResponse({"status": 500, "message": f"Internal Server Error: {err}"}, status=500)

