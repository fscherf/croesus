from django.core.management.base import BaseCommand

from ...utils.commands import NewLineTerminatorBuffer
from ...models import Person


class Command(BaseCommand):
    def handle(self, *args, **options):
        Person.objects.all().dump(NewLineTerminatorBuffer(self.stdout))
