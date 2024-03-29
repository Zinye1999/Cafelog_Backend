"""
URL configuration for cafelog_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from .views import HealthCheckViewSet
from rest_framework.routers import DefaultRouter

from core.web_urls import urlpatterns as web_urls

router = DefaultRouter()
router.register(r'', HealthCheckViewSet, basename='health-check')

urlpatterns = staticfiles_urlpatterns() + [
    path('api/', include([
        path('auth/', include('authentication.urls')),
        path('', include(router.urls)),
        path('', include('core.urls')),
    ])),
    path('', include(web_urls)),
]

print(urlpatterns)