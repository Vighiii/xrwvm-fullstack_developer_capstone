# Uncomment the imports before you add the code
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'

urlpatterns = [
    # Path for user registration
    path('register/', views.register_user, name='register'),

    # Path for user login
    path('login/', views.login_user, name='login'),

    # Path to view dealer reviews
    path('dealer_reviews/', views.dealer_reviews, name='dealer_reviews'),

    # Path to add a review
    path('add_review/', views.add_review, name='add_review'),

    # Path for the index page showing dealers list
    path('index/', views.index, name='index'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
