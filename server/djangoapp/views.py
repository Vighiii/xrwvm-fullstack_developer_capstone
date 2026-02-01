import json
import logging

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import CarMake, CarModel
from .populate import initiate
from .restapis import analyze_review_sentiments, get_request, post_review

# Get an instance of a logger
logger = logging.getLogger(__name__)


def get_cars(request):
    count = CarMake.objects.filter().count()
    if count == 0:
        initiate()

    car_models = CarModel.objects.select_related("car_make")
    cars = []

    for car_model in car_models:
        cars.append(
            {
                "CarModel": car_model.name,
                "CarMake": car_model.car_make.name,
            }
        )

    return JsonResponse({"CarModels": cars})


@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    username = data["userName"]
    password = data["password"]

    user = authenticate(username=username, password=password)
    response_data = {"userName": username}

    if user is not None:
        login(request, user)
        response_data["status"] = "Authenticated"

    return JsonResponse(response_data)


def logout_request(request):
    logout(request)
    return JsonResponse({"userName": ""})


@csrf_exempt
def registration(request):
    data = json.loads(request.body)

    username = data["userName"]
    password = data["password"]
    first_name = data["firstName"]
    last_name = data["lastName"]
    email = data["email"]

    try:
        User.objects.get(username=username)
        return JsonResponse(
            {"userName": username, "error": "Already Registered"}
        )
    except User.DoesNotExist:
        logger.debug("%s is new user", username)

    user = User.objects.create_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
        password=password,
        email=email,
    )

    login(request, user)
    return JsonResponse(
        {"userName": username, "status": "Authenticated"}
    )


def get_dealerships(request, state="All"):
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = f"/fetchDealers/{state}"

    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_reviews(request, dealer_id):
    if not dealer_id:
        return JsonResponse(
            {"status": 400, "message": "Bad Request"}
        )

    endpoint = f"/fetchReviews/dealer/{dealer_id}"
    reviews = get_request(endpoint)

    for review in reviews:
        sentiment = analyze_review_sentiments(
            review.get("review", "")
        )
        review["sentiment"] = sentiment

    return JsonResponse({"status": 200, "reviews": reviews})


def get_dealer_details(request, dealer_id):
    if not dealer_id:
        return JsonResponse(
            {"status": 400, "message": "Bad Request"}
        )

    endpoint = f"/fetchDealer/{dealer_id}"
    dealership = get_request(endpoint)
    return JsonResponse({"status": 200, "dealer": dealership})


def add_review(request):
    if request.user.is_anonymous:
        return JsonResponse(
            {"status": 403, "message": "Unauthorized"}
        )

    data = json.loads(request.body)

    try:
        post_review(data)
        return JsonResponse({"status": 200})
    except Exception as exc:
        logger.exception("Error in posting review: %s", exc)
        return JsonResponse(
            {"status": 401, "message": "Error in posting review"}
        )
