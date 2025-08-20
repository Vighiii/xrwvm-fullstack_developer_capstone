# Uncomment the required imports before adding the code
import json
import logging

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .models import CarMake, CarModel
from .populate import initiate
from .restapis import get_request, post_review

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Define backend URL using settings
BACKEND_URL = getattr(
    settings,
    "BACKEND_URL",
    (
        "https://lukaslondono-3030.theiadockernext-0-labs-prod-theiak8s-4-tor01."
        "proxy.cognitiveclass.ai"
    ),
).rstrip("/")


# ────────────────────────────────  AUTH  ──────────────────────────────────────
@csrf_exempt
def login_user(request):
    """API login from React (JSON)."""
    data = json.loads(request.body)
    username = data["userName"]
    password = data["password"]

    user = authenticate(username=username, password=password)
    payload = {"userName": username}

    if user is not None:
        login(request, user)
        payload["status"] = "Authenticated"

    return JsonResponse(payload)


def logout_request(request):
    """API logout (JSON)."""
    logout(request)
    return JsonResponse({"userName": ""})


@csrf_exempt
def registration(request):
    """API registration from React (JSON)."""
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
        pass

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


# ───────────────────────────────  DATA  ───────────────────────────────────────
def get_cars(request):
    """Return all car models/makes as JSON."""
    if CarMake.objects.count() == 0:
        initiate()

    car_models = CarModel.objects.select_related("car_make")
    cars = [
        {"CarModel": cm.name, "CarMake": cm.car_make.name}
        for cm in car_models
    ]
    return JsonResponse({"CarModels": cars})


def get_dealerships(request, state: str = "All"):
    """Return dealers list (optionally by state)."""
    endpoint = "/fetchDealers" if state == "All" else f"/fetchDealers/{state}"
    dealers = get_request(f"{BACKEND_URL}{endpoint}")
    return JsonResponse({"status": 200, "dealers": dealers})


def get_dealer_details(request, dealer_id: int):
    """Return single dealer detail by ID."""
    endpoint = f"/fetchDealer/{dealer_id}"
    dealership = get_request(f"{BACKEND_URL}{endpoint}")

    if not dealership:
        return JsonResponse({"status": 404, "message": "Dealer not found"})

    # Normaliza lista ↔︎ dict
    dealer_list = dealership if isinstance(dealership, list) else [dealership]
    return JsonResponse({"status": 200, "dealer": dealer_list})


def get_dealer_reviews(request, dealer_id: int):
    """Return reviews for a dealer (sentiment set to neutral)."""
    endpoint = f"/fetchReviews/dealer/{dealer_id}"
    reviews = get_request(f"{BACKEND_URL}{endpoint}")

    if reviews is None:
        return JsonResponse({"status": 404, "message": "No reviews found"})

    for review in reviews:
        review["sentiment"] = "neutral"

    return JsonResponse({"status": 200, "reviews": reviews})


@csrf_exempt
def add_review(request):
    """Post a new review (requires login)."""
    if request.user.is_anonymous:
        return JsonResponse({"status": 403, "message": "Unauthorized"})

    data = json.loads(request.body)
    try:
        post_review(data)
    except Exception as exc:  # noqa: BLE001  (explicit exception var)
        msg = f"Error in posting review: {exc}"
        return JsonResponse({"status": 401, "message": msg})

    return JsonResponse({"status": 200})


# ───────────────────────────  TEMPLATE VIEWS  ────────────────────────────────
def about(request):
    return render(request, "djangoapp/about.html")


def contact(request):
    return JsonResponse(
        {"status": 200, "message": "Contact endpoint is working"}
    )


# ────────── legacy template-based auth (kept for completeness) ───────────────
def login_request(request):
    context: dict[str, str] = {}

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["psw"]
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect("djangoapp:index")

        context["message"] = "Invalid username or password."

    return render(request, "djangoapp/login.html", context)


def registration_request(request):
    context: dict[str, str] = {}

    if request.method == "GET":
        return render(request, "djangoapp/registration.html", context)

    # POST
    username = request.POST["username"]
    password = request.POST["psw"]
    first_name = request.POST["firstname"]
    last_name = request.POST["lastname"]

    if User.objects.filter(username=username).exists():
        context["message"] = "User already exists."
        return render(request, "djangoapp/registration.html", context)

    user = User.objects.create_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
        password=password,
    )
    login(request, user)
    return redirect("djangoapp:index")
