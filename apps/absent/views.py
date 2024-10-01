from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins

from rest_framework.response import Response
from .models import Absent, AbsentType, AbsentStatusChoices
from .serializers import AbsentSerializer, AbsentTypeSerializer
from rest_framework.views import APIView
from .utils import get_responder
from apps.oaauth.serializers import UserSerializer


# Create your views here.
class AbsentViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = Absent.objects.all()
    serializer_class = AbsentSerializer

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        who=request.query_params.get('who')
        if who and who =='sub':
            result=queryset.filter(responder=request.user)
        else:
            result=queryset.filter(requester=request.user)

        serializer=self.serializer_class(result,many=True)
        return Response(data=serializer.data)

class AbsentTypeView(APIView):
    def get(self, request):
        types=AbsentType.objects.all()
        serializer=AbsentTypeSerializer(types,many=True)
        return Response(data=serializer.data)

class ResponderView(APIView):

    def get(self, request):
        responders=get_responder(request)
        serializer=UserSerializer(responders)
        return Response(data=serializer.data)
