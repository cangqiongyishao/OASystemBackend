from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import LoginSerializer, UserSerializer
from datetime import datetime
from .authentications import generate_jwt
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import ResetPwdSerializer
from rest_framework import status


# Create your views here.
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            user.last_login = datetime.now()
            user.save()
            token = generate_jwt(user)
            return Response({'token': token, 'user': UserSerializer(user).data})
        else:
            detail = list(serializer.errors.values())[0][0]
            return Response({'detail': detail}, status=status.HTTP_400_BAD_REQUEST)


# class AuthenticatedRequestView(APIView):
#     permission_classes = [IsAuthenticated]


class ResetPwdView(APIView):

    def post(self, request):
        serializer = ResetPwdSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            pwd1=serializer.validated_data.get('pwd1')
            request.user.set_password(pwd1)
            request.user.save()
            return Response()
        else:
            print(serializer.errors)
            detail = list(serializer.errors.values())[0][0]
        return Response({'detail': detail},status=status.HTTP_400_BAD_REQUEST)
