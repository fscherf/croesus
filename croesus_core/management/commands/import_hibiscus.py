from django.core.management.base import BaseCommand
from django.db import transaction

from ...utils.hibiscus import HibiscusProxy
from ...models import HibiscusTurnover


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--host', '-H', default='localhost')
        parser.add_argument('--port', '-P', default=18080)
        parser.add_argument('--no-verify', action='store_true', default=False)

    @transaction.atomic
    def handle(self, *args, **options):
        proxy = HibiscusProxy('admin', 'hibiscus', host=options['host'],
                              port=options['port'],
                              verify=not options['no_verify'])

        for turnover in proxy.turnovers():
            obj, created = HibiscusTurnover.objects.get_or_create(
                account_id=turnover['account_id'],
                turnover_id=turnover['turnover_id'])

            if created:
                for k, v in turnover.items():
                    setattr(obj, k, v)

                obj.save()

        HibiscusTurnover.objects.all().match_ibans()
