from rest_framework import serializers
from .models import OAUser, UserStatusChoices,OADepartment

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True,error_messages={"required":"Please enter your email"})
    password = serializers.CharField(max_length=20, min_length=6)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            user = OAUser.objects.filter(email=email).first()
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

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=OADepartment
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):

    department = DepartmentSerializer()
    class Meta:
        model=OAUser
        exclude=('password','groups','user_permissions')