from rest_framework import serializers
from .models import OAUser, UserStatusChoices,OADepartment
from rest_framework import exceptions

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

class ResetPwdSerializer(serializers.Serializer):
    oldpwd=serializers.CharField(min_length=6,max_length=20)
    pwd1=serializers.CharField(min_length=6,max_length=20)
    pwd2=serializers.CharField(min_length=6,max_length=20)

    def validate(self,attrs):
        oldpwd=attrs['oldpwd']
        pwd1=attrs['pwd1']
        pwd2=attrs['pwd2']

        user=self.context['request'].user
        if not user.check_password(oldpwd):
            raise exceptions.ValidationError('old password is incorrect')

        if pwd1 !=pwd2:
            raise exceptions.ValidationError('the two passwords do not match')
        return attrs