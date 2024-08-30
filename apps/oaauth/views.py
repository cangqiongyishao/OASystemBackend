from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import LoginSerializer,UserSerializer
from datetime import datetime
from .authentications import generate_jwt
from rest_framework.response import Response
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
            return Response({'token': token,'user':UserSerializer(user).data})
        else:
            print(serializer.errors)
            return Response({'detail':'parameter error'}, status=status.HTTP_400_BAD_REQUEST)
