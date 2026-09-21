from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'

urlpatterns = [
    # Authentication
    path('register', views.registration, name='register'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_request, name='logout'),

    # Cars
    path('get_cars', views.get_cars, name='get_cars'),

    # Dealer
    path('dealer/<int:dealer_id>', views.get_dealer, name='dealer'),

    # Reviews
    path(
        'reviews/dealer/<int:dealer_id>',
        views.get_dealer_reviews_page,
        name='dealer_reviews'
    ),

    path('add_review', views.add_review, name='add_review'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
