from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
from .models import Absent, AbsentType, AbsentStatusChoices
from .serializers import AbsentSerializer


# Create your views here.
class AbsentViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = Absent.objects.all()
    serializer_class = AbsentSerializer
