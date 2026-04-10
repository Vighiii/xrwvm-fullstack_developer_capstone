# Uncomment the required imports before adding the code

# from django.shortcuts import render
# from django.http import HttpResponseRedirect, HttpResponse
# from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404, render, redirect
# from django.contrib.auth import logout
# from django.contrib import messages
# from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
# from .populate import initiate

# Set up logger
logger = logging.getLogger(__name__)

def register_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            logger.warning(f"Registration failed: username '{username}' already exists.")
            return redirect('djangoapp:register')

        user = User.objects.create_user(username=username, password=password)
        user.save()
        messages.success(request, "Registration successful. Please log in.")
        logger.info(f"New user registered: {username}")
        return redirect('djangoapp:login')

    return render(request, 'register.html')


@csrf_exempt
def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect('djangoapp:index')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('djangoapp:login')

    return render(request, 'login.html')

# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
# def get_dealerships(request):
# ...

def logout_user(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect('djangoapp:login')

# Create a `get_dealer_details` view to render the dealer details
# def get_dealer_details(request, dealer_id):
# ...

def dealer_reviews(request):
    # Placeholder: replace with actual data fetching logic
    reviews = [
        {'dealer': 'Dealer One', 'review': 'Great service!', 'rating': 5},
        {'dealer': 'Dealer Two', 'review': 'Average experience.', 'rating': 3},
    ]
    context = {'reviews': reviews}
    return render(request, 'dealer_reviews.html', context)


def add_review(request):
    if request.method == "POST":
        # Placeholder: process form data and save review
        messages.success(request, "Review submitted successfully.")
        return redirect('djangoapp:dealer_reviews')

    return render(request, 'add_review.html')


def home(request):
    return render(request, 'Home.html')  # Ensure this template exists


def index(request):
    dealers = [
        {'name': 'Dealer One', 'location': 'New York', 'contact': '123-456-7890'},
        {'name': 'Dealer Two', 'location': 'Los Angeles', 'contact': '987-654-3210'},
    ]
    return render(request, 'index.html', {'dealers': dealers})