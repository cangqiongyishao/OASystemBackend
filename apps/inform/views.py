from rest_framework import viewsets
from rest_framework import mixins
from .models import Inform
from .serializers import InformSerializer


class InformViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = Inform.objects.all()
    serializer_class = InformSerializer
f