"""djangoproj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from djangoapp import views
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    path('djangoapp/', include('djangoapp.urls')),

    # Dealer and review APIs
    path('fetchDealers', views.get_dealerships, name='fetchDealers'),
    path('fetchDealer/<int:dealer_id>', views.get_dealer_details, name='fetchDealer'),
    path('fetchDealers/<str:state>', views.get_dealerships_by_state, name='fetchDealersByState'),
    path('fetchReviews/dealer/<int:dealer_id>', views.get_dealer_reviews, name='fetchDealerReviews'),
    path('analyze/<str:text>', views.analyze_review, name='analyzeReview'),

    path('', TemplateView.as_view(template_name="Home.html")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
