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
from .populate import initiate


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
    if request.method == 'POST':
        logout(request)
        data = {"message": "Successfully logged out", "userName": ""}
        return JsonResponse(data)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)

# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    if request.method == 'POST':
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)
            username = data.get('userName')
            password = data.get('password')
            first_name = data.get('firstName')
            last_name = data.get('lastName')
            email = data.get('email')

            # Check if any fields are missing
            if not all([username, password, first_name, last_name, email]):
                return JsonResponse({"error": "Missing required fields"}, status=400)

            # Check if the username already exists
            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "Username already exists"}, status=400)

            # Check if the email already exists
            if User.objects.filter(email=email).exists():
                return JsonResponse({"error": "Email already registered"}, status=400)

            # Create a new user
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password, email=email)

            # Log the user in after registration
            login(request, user)

            # Return successful registration
            return JsonResponse({"userName": username, "status": "Authenticated"}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)
    
# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
def get_dealerships(request):
    dealerships = [
        {'id': 1, 'name': 'Dealer One', 'location': 'City A'},
        {'id': 2, 'name': 'Dealer Two', 'location': 'City B'},
        # Add more dealership data or fetch from API/DB
    ]

    return render(request, 'index.html', {'dealerships': dealerships})

# Create a `get_dealer_reviews` view to render the reviews of a dealer
def get_dealer_reviews(request, dealer_id):
    # Simulate dealer reviews or fetch from API/DB
    reviews = [
        {'review': 'Great service!', 'rating': 5, 'dealer_id': dealer_id},
        {'review': 'Not bad', 'rating': 3, 'dealer_id': dealer_id},
    ]

    return render(request, 'dealer_reviews.html', {'reviews': reviews, 'dealer_id': dealer_id})
# Create a `get_dealer_details` view to render the dealer details
def get_dealer_details(request, dealer_id):
    # Simulate dealer details or fetch from API/DB
    dealer = {'id': dealer_id, 'name': 'Dealer One', 'location': 'City A'}
    
    return render(request, 'dealer_details.html', {'dealer': dealer})

# Create a `add_review` view to submit a review
def add_review(request):
    if request.method == 'POST':
        dealer_id = request.POST.get('dealer_id')
        review = request.POST.get('review')
        rating = request.POST.get('rating')

        # Simulate saving the review (normally save it in DB or call an API)
        print(f'Review: {review}, Rating: {rating}, Dealer ID: {dealer_id}')
        
        return redirect('get_dealer_reviews', dealer_id=dealer_id)  # Redirect to reviews page

    # Render the review form if it's a GET request
    return render(request, 'add_review.html')