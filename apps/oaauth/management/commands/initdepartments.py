from django.core.management.base import BaseCommand
from apps.oaauth.models import OADepartment

class Command(BaseCommand):
    def handle(self, *args, **options):
        boarder = OADepartment.objects.create(name="Board of Directors", intro="Board of Directors")
        developer = OADepartment.objects.create(name="Product Development",
                                                intro="Product Design, Technology Development")
        operator = OADepartment.objects.create(name="Operations", intro="Customer Operations, Product Operations")
        saler = OADepartment.objects.create(name="Sales", intro="Product Sales")
        hr = OADepartment.objects.create(name="Human Resources",
                                         intro="Employee Recruitment, Employee Training, Employee Assessment")
        finance = OADepartment.objects.create(name="Finance", intro="Financial Reporting, Financial Review")
        self.stdout.write('Departments data initial successfully created')

