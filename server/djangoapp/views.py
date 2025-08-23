from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.views.decorators.csrf import csrf_exempt
import logging
import json
from datetime import datetime
from .populate import initiate

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.

# Create a `login_user` view to handle sign in request
@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        # Get username and password from request body (JSON)
        data = json.loads(request.body)
        username = data.get('userName')
        password = data.get('password')

        # Try to authenticate the user
        user = authenticate(username=username, password=password)

        if user is not None:
            # If authentication is successful, log the user in
            login(request, user)
            response_data = {"userName": username, "status": "Authenticated"}
        else:
            # Authentication failed
            response_data = {"status": "Error", "message": "Invalid credentials"}

        return JsonResponse(response_data)
    
    # If not POST, return an error
    return JsonResponse({"status": "Error", "message": "Invalid request method"}, status=400)

# Create a `logout_user` view to handle logout request
def logout_user(request):
    # Log the user out
    logout(request)
    
    # Return a JSON response
    data = {"userName": ""}
    return JsonResponse(data)

# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    try:
        if request.method == 'POST':
            # Load the JSON data from the request
            data = json.loads(request.body)

            # Extract user details from the request body
            username = data.get('userName')
            password = data.get('password')
            first_name = data.get('firstName')
            last_name = data.get('lastName')
            email = data.get('email')

            # Check if any required fields are missing
            if not all([username, password, first_name, last_name, email]):
                return JsonResponse({"error": "Missing fields"}, status=400)

            # Check if the username already exists
            if User.objects.filter(username=username).exists():
                return JsonResponse({"userName": username, "error": "Already Registered"}, status=400)

            # Create the new user
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email
            )

            # Log in the user after creation
            login(request, user)

            # Return success response
            return JsonResponse({"userName": username, "status": "Authenticated"}, status=201)

        else:
            return JsonResponse({"error": "Invalid request method"}, status=400)

    except Exception as e:
        # Log the exact error for debugging purposes
        logger.error(f"Error during registration: {str(e)}")
        return JsonResponse({"error": "Server Error", "details": str(e)}, status=500)


# Update the `get_dealerships` view to render the index page with a list of dealerships
# def get_dealerships(request):
#     ...

# Create a `get_dealer_reviews` view to render the reviews of a dealer
# def get_dealer_reviews(request, dealer_id):
#     ...

# Create a `get_dealer_details` view to render the dealer details
# def get_dealer_details(request, dealer_id):
#     ...

# Create a `add_review` view to submit a review
# def add_review(request):
#     ...
