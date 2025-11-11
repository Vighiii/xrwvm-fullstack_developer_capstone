# Uncomment the imports before you add the code
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # # path for registration
    path('register/', views.registration, name='register'),  

    # path for login
    path(route='login', view=views.login_user, name='login'),

    # path for dealer reviews view
    path('dealer/<int:dealer_id>/reviews/', views.get_dealer_reviews, name='get_dealer_reviews'), 

    # path for add a review view
    path('add_review/', views.add_review, name='add_review'), 
    
    path('logout/', views.logout_request, name='logout'), 
    path('dealer/<int:dealer_id>/', views.get_dealer_details, name='get_dealer_details'),  
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
