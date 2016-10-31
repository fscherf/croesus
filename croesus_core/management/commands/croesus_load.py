from django.core.management.base import BaseCommand, CommandError
from django.core import management
from django.db import transaction
from django.apps import apps


class ImplementationError(CommandError):
    pass


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

        self.models = {
            i._meta.object_name: i for i in
            apps.get_app_config('croesus_core').get_models()
        }

    def add_arguments(self, parser):
        parser.add_argument('fixtures', nargs='+')

    def clear_table(self, model_name):
        self.models[model_name].objects.all().delete()
        self.models.pop(model_name)

    def clear_all_tables(self):
        for model_name in list(self.models.keys()):
            self.clear_table(model_name)

    @transaction.atomic
    def handle(self, *args, **options):
        self.clear_table('Booking')
        self.clear_all_tables()

        self.load(options['fixtures'])

    def load(self, fixtures):
        if self.models:
            raise ImplementationError('Not all tables are cleared')

        management.call_command('loaddata', *fixtures)
