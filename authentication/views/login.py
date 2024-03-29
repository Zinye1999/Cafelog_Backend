from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request

from django.http.response import HttpResponseBadRequest, HttpResponseServerError
from django.utils import timezone

from model.models import TemporaryPassword, User

from utils.jwt import jwt_encode
from utils.send_email import send_html_email
from django.conf import settings

class LoginViewSet(ViewSet):
    
    @action(detail=False, methods=["POST"])
    def request_password(self, request: Request):
        email = request.data.get("email", None)
        if not isinstance(email, str):
            return HttpResponseBadRequest()
        email = email.lower()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create(email=email, username=email, name=f"User-{email}")
        temp_password, created = TemporaryPassword.objects.get_or_create(for_user=user)
        if temp_password.expired < timezone.now():
            temp_password.expired = timezone.now() + timezone.timedelta(minutes=15)
            temp_password.save()
        # send password to email
        context = {
            "base_url": settings.CLIENT_BASE_URL,
            "email": user.email,
            "password": temp_password.password,
        }
        send_html_email('email/request_password', f'Login code for user cafelog {email}', email, context)
        return Response({"message": "ok"})
    
    @action(detail=False, methods=["POST"])
    def login(self, request: Request):
        email = request.data.get("email", None)
        password = request.data.get("password", None)
        print(email,password)
        if email is None or password is None:
            return Response({"message": "email or password is empty"})
        try:
            user = User.objects.get(email=email)
            temp_password = TemporaryPassword.objects.get(for_user=user)
        except  User.DoesNotExist:
            print("Usererror")
            return HttpResponseBadRequest()
        except  TemporaryPassword.DoesNotExist:
            return HttpResponseServerError()
        if temp_password.expired < timezone.now() or temp_password.password != password:
            print(temp_password.expired,timezone.now())
            return HttpResponseBadRequest()
        temp_password.delete()
        user_payload = user.for_auth()
        token, _ = jwt_encode(user_payload)
        # TODO: register token

        return Response({
            "token": token,
            "payload": user_payload
        })