
from django.urls import path, include

from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'profile', ProfileViewSet, "profile")
router.register(r'cafe', CafeViewSet, "cafe")
router.register(r'review', CafeReviewViewSet, "cafe_review")
router.register(r'follow', UserFollowViewSet, "user_follow")
router.register(r'following', UserFollowingsViewSet, "user_following")
router.register(r'follower', UserFollowersViewSet, "user_follower")
router.register(r'upload_image', UploadImageViewSet, "upload_image")

urlpatterns = [
    path("", include(router.urls))
]