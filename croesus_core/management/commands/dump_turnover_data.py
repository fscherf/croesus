from django.core.management.base import BaseCommand

from ...utils.commands import NewLineTerminatorBuffer
from ...models import HibiscusTurnover


class Command(BaseCommand):
    def handle(self, *args, **options):
        HibiscusTurnover.objects.all().dump(
            NewLineTerminatorBuffer(self.stdout))
