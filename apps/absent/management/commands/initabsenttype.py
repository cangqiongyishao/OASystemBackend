from django.core.management.base import BaseCommand
from apps.absent.models import AbsentType

class Command(BaseCommand):
    def handle(self, *args, **options):
        absent_types = [
            "Personal Leave",
            "Sick Leave",
            "Work Injury Leave",
            "Marriage Leave",
            "Funeral Leave",
            "Maternity Leave",
            "Paternity Leave",
            "Visiting Family Leave",
            "Public Holiday",
            "Annual Leave"
        ]
        absents=[]
        for absent_type in absent_types:
            absents.append(AbsentType(name=absent_type))
        AbsentType.objects.bulk_create(absents)
        self.stdout.write('absents type initial success')
