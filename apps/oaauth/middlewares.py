from django.utils.deprecation import MiddlewareMixin
from rest_framework.authentication import get_authorization_header
from rest_framework import exceptions
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http.response import JsonResponse
from rest_framework.status import HTTP_403_FORBIDDEN
from jwt.exceptions import ExpiredSignatureError
from django.contrib.auth.models import AnonymousUser

OAUser=get_user_model()

class LoginCheckMiddleware(MiddlewareMixin):
    keyword='JWT'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 对于那些不需要登录就能访问的接口，可以写在这里
        self.white_list = ['/auth/login/','/auth/register/']
    def process_view(self,request,view_func,view_args,view_kwargs):

        if request.path == '/auth/login':
            request.user=AnonymousUser()
            request.auth=None
            return None

        try:
            auth = get_authorization_header(request).split()
            if not auth or auth[0].lower() != self.keyword.lower().encode():
                raise exceptions.ValidationError('Please send a valid JWT')

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
                    request.user=user
                    request.auth=jwt_token

                except:
                    msg = "User does not exist!"
                    raise exceptions.AuthenticationFailed(msg)
            except ExpiredSignatureError:
                msg = "JWT Token has expired!"
                raise exceptions.AuthenticationFailed(msg)

        except Exception as e:
            print(e)

            return JsonResponse(data={'detail':'Please login first'}, status=HTTP_403_FORBIDDEN)

