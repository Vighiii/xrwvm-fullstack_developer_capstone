from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('djangoapp/', include('djangoapp.urls')),

    # مسارات واجهة React المستضافة داخل Django
    path('', TemplateView.as_view(template_name="index.html")),
    path('about/', TemplateView.as_view(template_name="index.html")),
    path('contact/', TemplateView.as_view(template_name="index.html")),
    path('login/', TemplateView.as_view(template_name="index.html")),
    path('register/', TemplateView.as_view(template_name="index.html")),
    path('dealers/', TemplateView.as_view(template_name="index.html")),
    path(
        'dealer/<int:dealer_id>',
        TemplateView.as_view(
            template_name="index.html")),

    # السطر الجديد المطلوب لحل مشكلة الـ 404 وعرض صفحة كتابة المراجعة للـ React
    path(
        'postreview/<int:dealer_id>',
        TemplateView.as_view(
            template_name="index.html")),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
