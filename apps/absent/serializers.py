from rest_framework import serializers
from .models import Absent, AbsentType
from apps.oaauth.serializers import UserSerializer


class AbsentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbsentType
        fields = '__all__'


class AbsentSerializer(serializers.ModelSerializer):
    absent_type=AbsentTypeSerializer(read_only=True)
    absent_type_id=serializers.IntegerField(write_only=True)
    requester=UserSerializer(read_only=True)
    responder=UserSerializer(read_only=True)

    class Meta:
        model = Absent
        fields = '__all__'
