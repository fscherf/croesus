import datetime

from django.core.management.base import BaseCommand

from ...models import MembershipFeeDebt


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('year', type=int)
        parser.add_argument('month', type=int)

    def handle(self, *args, **options):
        period = datetime.date(options['year'], options['month'], 1)

        MembershipFeeDebt.objects.create_for(period)
