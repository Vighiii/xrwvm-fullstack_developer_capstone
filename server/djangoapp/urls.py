from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'

urlpatterns = [
    # Registration
    path('register', views.registration, name='register'),

    # Login
    path('login', views.login_user, name='login'),

    # Logout
    path('logout', views.logout_request, name='logout'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
