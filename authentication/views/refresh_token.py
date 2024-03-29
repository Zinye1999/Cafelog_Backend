from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request

from model.models import User

from utils.jwt import jwt_encode
from authentication.utils import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class RefreshTokenViewSet(ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=["PUT"])
    def refresh_token(self, request: Request):
        user: User = request.user
        user_payload = user.for_auth()
        refresh_token, _ = jwt_encode(user_payload)
        # TODO: unregister token

        return Response({
            "refresh_token": refresh_token,
            "payload": user_payload
        })