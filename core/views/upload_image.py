import os
from pathlib import Path
from PIL import Image
from datetime import datetime
# from typing import cast, Self
from typing_extensions import Self

from django.conf import settings
from django.core.files.uploadedfile import UploadedFile

from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request

from authentication.utils import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from model.models import User


BASE_DIR = settings.BASE_DIR

ACCEPT_CONTENT_TYPES = ["image/jpeg", "image/png"]

class UploadImageViewSet(ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=["POST"])
    def upload_profile(self: Self, request: Request):
        user: User = request.user
        file: UploadedFile = request.FILES["file"]
        if file.content_type not in ACCEPT_CONTENT_TYPES:
            return Response({"message": "Content type is not accepted"}, status=400)
        date = datetime.now().strftime("%Y%m%d%H%M%S%f")
        base_path = os.path.join("static", "images", "users", f"{user.id}{date}.png")
        with Image.open(file) as img:
            img.save(os.path.join(BASE_DIR, base_path))
        if user.profile_picture is not None:
            Path(os.path.join(BASE_DIR, user.profile_picture)).unlink(missing_ok=True)
        user.profile_picture = base_path
        user.save()
        return Response({"files": [base_path]})
    
    
    @action(detail=True, methods=["POST"])
    def upload_reviews(self: Self, request: Request, pk=None):
        user: User = request.user
        if pk is None:
            pk = 0
        paths = []
        file: UploadedFile = request.FILES["file"]
        # for key, file in request.FILES.items():
        # file = cast(UploadedFile, file)
        # print("Upload file key:", key)
        if file.content_type not in ACCEPT_CONTENT_TYPES:
            for p in paths:
                Path(os.path.join(BASE_DIR, p)).unlink(missing_ok=True)
            return Response({"message": f"filename: {file.name}, content type is not accepted"}, status=400)
        date = datetime.now().strftime("%Y%m%d%H%M%S%f")
        base_path = os.path.join("static", "images", "reviews", f"{user.id}{date}-{pk}.png")
        with Image.open(file) as img:
            img.save(os.path.join(BASE_DIR, base_path))
        paths.append(base_path)
        return Response({"files": paths})