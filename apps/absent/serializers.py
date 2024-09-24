from rest_framework import serializers
from .models import Absent, AbsentType, AbsentStatusChoices
from apps.oaauth.serializers import UserSerializer
from rest_framework import exceptions


class AbsentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbsentType
        fields = '__all__'


class AbsentSerializer(serializers.ModelSerializer):
    absent_type = AbsentTypeSerializer(read_only=True)
    absent_type_id = serializers.IntegerField(write_only=True)
    requester = UserSerializer(read_only=True)
    responder = UserSerializer(read_only=True)

    class Meta:
        model = Absent
        fields = '__all__'

    def validate_absent_type_id(self, value):
        if not AbsentType.objects.filter(pk=value).exists():
            raise exceptions.ValidationError("The absent type does not exist")
        return value


    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        if user.department.leader.uid == user.uid:
            if user.department.name == 'Board of Directors':
                responder = None
            else:
                responder = user.department.manager
        else:
            responder = user.department.leader

        if responder is None:
            validated_data['status'] = AbsentStatusChoices.PASS

        absent = Absent.objects.create(**validated_data, requester=user, responder=responder)
        return absent

    def update(self, instance, validated_data):
        if instance.status != AbsentStatusChoices.AUDITING:
            raise exceptions.APIException(detail="can't change the status of processed absent")
        request = self.context['request']
        user = request.user

        if instance.responder.uid != user.uid:
            raise exceptions.AuthenticationFailed(detail="You don't have permission to perform this action")
        instance.status = validated_data['status']
        instance.response_content = validated_data['response_content']
        instance.save()
        return instance
