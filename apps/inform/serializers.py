from rest_framework import serializers
from .models import Inform,InformRead
from apps.oaauth.serializers import UserSerializer,DepartmentSerializer
from apps.oaauth.models import OADepartment

class InformSerializer(serializers.ModelSerializer):
    author=UserSerializer(read_only=True)
    departments=DepartmentSerializer(many=True,read_only=True)
    department_id=serializers.ListField(write_only=True)


    class Meta:
        model=Inform
        fields='__all__'

    def create(self,validated_data):
        request=self.context['request']
        department_ids=validated_data.pop('department_id')

        map(lambda value:int(value),department_ids)
        if 0 in department_ids:
            inform=Inform.objects.create(public=True,author=request.user,**validated_data)
        else:
            departments=OADepartment.objects.filter(id__in=department_ids).all()
            inform=Inform.objects.create(public=False,author=request.user,**validated_data)
            inform.departments.set(departments)
            inform.save()
        return inform

