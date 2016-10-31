from django.core.management.base import BaseCommand
from django.core import management


class Command(BaseCommand):
    def handle(self, *args, **options):
        management.call_command('dumpdata', 'croesus_core')
