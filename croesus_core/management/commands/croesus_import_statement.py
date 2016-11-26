from django.core.management.base import BaseCommand, CommandError
from django.db import transaction as db_transaction

from croesus_core.models.bank import Statement, Transaction
from croesus_core.utils.mt940 import parse_mt940

import os


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('files', nargs='+')

    @db_transaction.atomic
    def handle(self, *args, **options):
        for path in options['files']:
            data = open(path, 'r').read()
            transactions = parse_mt940(data)

            if not transactions.data:
                raise CommandError('{} does not contain valid MT940'.format(path))  # NOQA

            statement = Statement.objects.create(
                format='MT940',
                data=data,
                file_name=os.path.basename(path),
            )

            added_objects = Transaction.objects.parse_statement(statement)

            self.stdout.write('Added {} transaction(s)'.format(added_objects))
