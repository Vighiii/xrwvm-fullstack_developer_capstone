import os
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.views.static import serve
from django.conf.urls.static import static
from django.conf import settings

FRONTEND_BUILD_DIR = os.path.join(settings.BASE_DIR, "frontend", "build")

urlpatterns = [
    path('admin/', admin.site.urls),

    # Backend API
    path('djangoapp/', include('djangoapp.urls')),

    # Django pages
    path('', TemplateView.as_view(template_name="Home.html")),
    path('about/', TemplateView.as_view(template_name="About.html")),
    path('contact/', TemplateView.as_view(template_name="Contact.html")),

    # React pages
    path('login/', TemplateView.as_view(template_name="index.html")),
    path('register/', TemplateView.as_view(template_name="index.html")),
    path('dealers/', TemplateView.as_view(template_name="index.html")),

    # React public build files
    re_path(r'^manifest\.json$', serve, {
        'path': 'manifest.json',
        'document_root': FRONTEND_BUILD_DIR,
    }),
    re_path(r'^favicon\.ico$', serve, {
        'path': 'favicon.ico',
        'document_root': FRONTEND_BUILD_DIR,
    }),
    re_path(r'^logo192\.png$', serve, {
        'path': 'logo192.png',
        'document_root': FRONTEND_BUILD_DIR,
    }),
    re_path(r'^logo512\.png$', serve, {
        'path': 'logo512.png',
        'document_root': FRONTEND_BUILD_DIR,
    }),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )
