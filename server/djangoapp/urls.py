from django.urls import path
from . import views

urlpatterns = [
    path('get_dealers/', views.get_dealership, name='get_dealers'),
    path(
        'get_dealers/<str:state>/',
        views.get_dealership,
        name='get_dealers_by_state',
    ),
]
