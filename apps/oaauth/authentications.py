import jwt
import time
from django.conf import settings
from rest_framework.authentication import BaseAuthentication,get_authorization_header
from rest_framework import exceptions
from jwt.exceptions import ExpiredSignatureError
from .models import OAUser

def generate_jwt(user):
    expire_time=time.time()+60*60*24*7
    return jwt.encode({'userid':user.pk,'exp':expire_time},key=settings.SECRET_KEY)

class JWTAuthentication(BaseAuthentication):
    keyword='JWT'
    def authenticate(self, request):
        auth = request.headers.get('Authorization', '').split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = "Invalid JWT header!"
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = "Invalid JWT header! JWT Token should not contain spaces!"
            raise exceptions.AuthenticationFailed(msg)

        try:
            jwt_token = auth[1]
            jwt_info = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms='HS256')
            userid = jwt_info.get('userid')

            try:
                # Attach the current user to the request object
                user = OAUser.objects.get(pk=userid)
                setattr(request, 'user', user)
                return user, jwt_token
            except:
                msg = "User does not exist!"
                raise exceptions.AuthenticationFailed(msg)
        except jwt.ExpiredSignatureError:
            msg = "JWT Token has expired!"
            raise exceptions.AuthenticationFailed(msg)