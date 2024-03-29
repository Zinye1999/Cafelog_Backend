from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request

class LogoutViewSet(ViewSet):
    
    @action(detail=False, methods=["POST"])
    def logout(self, request: Request):
        token = request.data.get("token", None)
        # TODO: unregister token
        
        return Response(status=200)