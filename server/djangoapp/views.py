from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .populate import initiate
from .models import CarMake, CarModel
from .restapis import get_request, analyze_review_sentiments, post_review
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create a `login_request` view to handle sign-in request
@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']

    # Authenticate user
    user = authenticate(username=username, password=password)
    response_data = {"userName": username}

    if user:
        login(request, user)
        response_data["status"] = "Authenticated"
    return JsonResponse(response_data)


# Create a `logout_request` view to handle sign-out request
def logout_request(request):
    logout(request)
    return JsonResponse({"userName": ""})


# Create a `registration` view to handle sign-up request
@csrf_exempt
def registration(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']

    try:
        # Check if the user already exists
        User.objects.get(username=username)
        return JsonResponse({"userName": username,
                             "error": "Already Registered"})
    except User.DoesNotExist:
        logger.debug(f"{username} is a new user")

    # Create a new user and log them in
    user = User.objects.create_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
        password=password,
        email=email
    )
    login(request, user)
    return JsonResponse({"userName": username, "status": "Authenticated"})


# Get dealerships, optionally filtered by state
def get_dealerships(request, state="All"):
    endpoint = f"/fetchDealers/{state}" if state != "All" else "/fetchDealers"
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


# Get reviews for a specific dealer
def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews = get_request(endpoint)

        for review_detail in reviews:
            sentiment = analyze_review_sentiments(review_detail['review'])
            review_detail['sentiment'] = sentiment['sentiment']

        return JsonResponse({"status": 200, "reviews": reviews})
    return JsonResponse({"status": 400, "message": "Bad Request"})


# Get details for a specific dealer
def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchDealer/{dealer_id}"
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    return JsonResponse({"status": 400, "message": "Bad Request"})


# Add a new review
def add_review(request):
    if not request.user.is_anonymous:
        data = json.loads(request.body)
        try:
            post_review(data)
            return JsonResponse({"status": 200})
        except Exception:
            return JsonResponse({"status": 401, "message":
                                 "Error in posting review"})
    return JsonResponse({"status": 403, "message": "Unauthorized"})


# Get cars and initiate population if none exist
def get_cars(request):
    if CarMake.objects.count() == 0:
        initiate()

    car_models = CarModel.objects.select_related('car_make').all()
    cars = [
        {"CarModel": cm.name, "CarMake": cm.car_make.name}
        for cm in car_models
    ]
    return JsonResponse({"CarModels": cars})
