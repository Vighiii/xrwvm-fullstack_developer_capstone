from django.urls import path, re_path
from django.views.generic import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf import settings
from django.conf.urls.static import static
from . import views


app_name = 'djangoapp'
urlpatterns = [
    path(route='add_review', view=views.add_review, name='add_review'),
    path(route='reviews/dealer/<int:dealer_id>', view=views.get_dealer_reviews, name='dealer_details'),
    path(route='dealer/<int:dealer_id>', view=views.get_dealer_details, name='dealer_details'),
    path(route='get_dealers', view=views.get_dealerships, name='get_dealers'),
    path(route='get_dealers/<str:state>', view=views.get_dealerships, name='get_dealers_by_state'),
    path(route='get_cars', view=views.get_cars, name ='getcars'),
    path(route='register', view=views.register, name='register'),
    path(route='logout', view=views.logout_request, name='logout'),
    path(route='login', view=views.login_user, name='login'),
    re_path(r'^favicon\.ico$', RedirectView.as_view(url=staticfiles_storage.url('favicon.ico'), permanent=True)),
    re_path(r'^manifest\.json$', RedirectView.as_view(url=staticfiles_storage.url('manifest.json'), permanent=True)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)