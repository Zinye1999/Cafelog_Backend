from rest_framework.viewsets import ViewSet

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request

class HealthCheckViewSet(ViewSet):
    
    @action(detail=False, methods=["GET"])
    def health(self, _: Request):
        return Response({"message": "ok"})
    
    @action(detail=False, methods=["GET"])
    def ping(self, _: Request):
        return Response({"message": "pong"})
    
    