from rest_framework.routers import DefaultRouter

from .views import LoginViewSet, LogoutViewSet, RefreshTokenViewSet

router = DefaultRouter()
router.register(r'', LoginViewSet, basename='login')
router.register(r'', LogoutViewSet, basename='logout')
router.register(r'', RefreshTokenViewSet, basename='refresh-token')

from django.urls import path, include

urlpatterns = [
    path('', include(router.urls))
]