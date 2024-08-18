from django.core.management.base import BaseCommand
from apps.oaauth.models import OAUser,OADepartment

class Command(BaseCommand):
    def handle(self, *args, **options):
        boarder = OADepartment.objects.get(name="Board of Directors")
        developer = OADepartment.objects.get(name="Product Development")
        operator = OADepartment.objects.get(name="Operations")
        saler = OADepartment.objects.get(name="Sales")
        hr = OADepartment.objects.get(name="Human Resources")
        finance = OADepartment.objects.get(name="Finance")

        dongdong=OAUser.objects.create_superuser(email='dongdong111@gmail.com',
                        realname='dongdong',
                        password='111111',
                        department=boarder)
        duoduo=OAUser.objects.create_superuser(email='duoduo111@gmail.com',
                                               realname='duoduo',
                                               password='111111',
                                               department=boarder)
        Zhang=OAUser.objects.create_superuser(email='zhang111@gmail.com',
                                               realname='Zhang',
                                               password='111111',
                                               department=developer)

        Lee=OAUser.objects.create_user(email='li111@gmail.com',
                                               realname='Lee',
                                               password='111111',
                                               department=operator)
        Wang=OAUser.objects.create_user(email='wang111@gmail.com',
                                               realname='Wang',
                                               password='111111',
                                               department=hr)
        Zhao=OAUser.objects.create_user(email='zhao111@gmail.com',
                                               realname='Zhao',
                                               password='111111',
                                               department=finance)
        Sun=OAUser.objects.create_user(email='sun111@gmail.com',
                                               realname='Sun',
                                               password='111111',
                                               department=saler)

        boarder.leader=dongdong
        boarder.manager=None

        developer.leader=Zhang
        developer.manager=dongdong

        operator.leader=Lee
        operator.manager=dongdong

        saler.leader=Sun
        saler.manager=dongdong

        hr.leader=Wang
        hr.manager=duoduo

        finance.leader=Zhao
        finance.manager=duoduo

        boarder.save()
        developer.save()
        operator.save()
        saler.save()
        hr.save()
        finance.save()

        self.stdout.write('initial user successfully created')





