from rest_framework import serializers
from .models import OAUser, UserStatusChoices

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(max_length=20, min_length=6)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            user = OAUser.objects.get(email=email)
            if not user:
                raise serializers.ValidationError('Please check your email')
            if not user.check_password(password):
                raise serializers.ValidationError('Please check your password')
            if user.status == UserStatusChoices.INACTIVATED:
                raise serializers.ValidationError('The user is not activated')
            elif user.status == UserStatusChoices.LOCKED:
                raise serializers.ValidationError('The user is locked, contact administrator')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Please enter correct email and password')
        return attrs
