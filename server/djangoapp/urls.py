# Uncomment the imports before you add the code
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    path('login', view=views.login_user, name='login'),
    path('logout', view=views.logout_user, name='logout'),
    path('register', view=views.registration, name='register'),
    path('get_dealers/', view=views.get_dealerships, name='get_dealers'),
    path('get_dealers/<str:state>', view=views.get_dealerships, name='get_dealers_by_state'),
    path('dealer_reviews/<int:dealer_id>', view=views.get_dealer_reviews, name='dealer_reviews'),
    path('dealer_details/<int:dealer_id>', view=views.get_dealer_details, name='dealer_details'),
    path('add_review', view=views.add_review, name='add_review'),
    path('get_cars', view=views.get_cars, name='getcars'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
