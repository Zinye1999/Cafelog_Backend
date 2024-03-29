
from rest_framework.response import Response
from rest_framework.request import Request
from .auth_class import TokenAuthentication
from functools import wraps

def token_auth_viewset_func(func):
    def _response(msg):
        return Response({"message": msg}, status=401)
    auth_class = TokenAuthentication()
    @wraps(func)
    def wrapper(self, request: Request, *args, **kwargs):
        try:
            user = auth_class.authenticate(request)
            if user is None:
                return _response("not_authenticated")
            request.user = user[0]
            return func(self, request, *args, **kwargs)
        except Exception as e:
            return _response(str(e))
    return wrapper

def token_is_auth_viewset_func(func):
    def _response(msg):
        return Response({"message": msg}, status=401)
    def wrapper(self, request: Request, *args, **kwargs):
        check = bool(request.user and request.user.is_authenticated)
        if check:
            return func(self, request, *args, **kwargs)
        return _response("forbidden")
    return wrapper

def token_is_admin_auth_viewset_func(func):
    def _response(msg):
        return Response({"message": msg}, status=401)
    def wrapper(self, request: Request, *args, **kwargs):
        check = bool(request.user and request.user.is_authenticated and request.user.is_staff)
        if check:
            return func(self, request, *args, **kwargs)
        return _response("forbidden")
    return wrapper