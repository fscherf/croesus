from datetime import date

from django.core.management.base import BaseCommand

from ...reports import render_report


class Command(BaseCommand):
    def add_arguments(self, parser):
        today = date.today()

        parser.add_argument('--year', '-y', type=int, default=today.year)
        parser.add_argument('--month', '-m', type=int, default=today.month)

        parser.add_argument('--template', '-t', type=str,
                            default='mediawiki_de')

        parser.add_argument('--debug', '-d', action='store_true')

    def handle(self, *args, **options):
        self.stdout.write(
            render_report(
                options['year'],
                options['month'],
                options['template'],
                debug_buffer=self.stderr if options['debug'] else None,
            ),
        )
