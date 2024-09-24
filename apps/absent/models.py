from django.db import models
from django.contrib.auth import get_user_model

OAUser=get_user_model()

class AbsentStatusChoices(models.IntegerChoices):
    AUDITING = 1
    PASS = 2
    REJECT = 3

class AbsentType(models.Model):
    name = models.CharField(max_length=100)
    create_time = models.DateTimeField(auto_now_add=True)

class Absent(models.Model):
    title = models.CharField(max_length=200)
    request_content= models.TextField()
    absent_type = models.ForeignKey(AbsentType, on_delete=models.CASCADE,related_name='absents',related_query_name='absents')
    requester= models.ForeignKey(OAUser, on_delete=models.CASCADE,related_name='my_absents',related_query_name='my_absents')
    responder= models.ForeignKey(OAUser, on_delete=models.CASCADE,related_name='sub_absents',related_query_name='sub_absents',null=True)
    status=models.IntegerField(choices=AbsentStatusChoices, default=AbsentStatusChoices.AUDITING)
    start_date= models.DateTimeField()
    end_date= models.DateTimeField()
    create_time = models.DateTimeField(auto_now_add=True)
    response_content=models.TextField(blank=True)

