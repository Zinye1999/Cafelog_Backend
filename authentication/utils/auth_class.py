import binascii

from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework import exceptions

from django.utils.translation import gettext_lazy as _

from model.models import User

from utils.jwt import jwt_decode

class TokenAuthentication(BaseAuthentication):

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != b'token':
            return None
        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. Credentials string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)
        try:
            try:
                auth_decoded = auth[1].decode('utf-8')
            except UnicodeDecodeError:
                auth_decoded = auth[1].decode('latin-1')
        except (TypeError, UnicodeDecodeError, binascii.Error):
            msg = _('Invalid token header. Credentials not correctly base64 encoded.')
            raise exceptions.AuthenticationFailed(msg)
        try:
            payload = jwt_decode(auth_decoded)
        except Exception:
            msg = _('Invalid token. Decode failed')
            raise exceptions.AuthenticationFailed(msg)
        user_id = payload.get("id", None)
        user_email = payload.get("email", None)
        if user_email is None or user_id is None:
            msg = _('Invalid token header. Credentials not correctly.')
            raise exceptions.AuthenticationFailed(msg)
        try:
            user: User = User.objects.get(id=user_id, email=user_email)
        except User.DoesNotExist:
            msg = _('Not found user')
            raise exceptions.AuthenticationFailed(msg)
        except User.MultipleObjectsReturned:
            print("user id:", user_id)
            print("user email:", user_email)
            msg = _('Server error')
            raise exceptions.AuthenticationFailed(msg)
        return (user, None)