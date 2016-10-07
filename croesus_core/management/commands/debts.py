from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from ...models import MembershipFeeDebt, HibiscusTurnover, Account

from ...utils.shell import (
    queryset_to_prettytable,
    confirmation_prompt,
    option_prompt,
    range_prompt,
    green,
    blue,
    echo,
    red,
)

from datetime import date


class Command(BaseCommand):
    HIBISCUS_TURNOVER_FIELDS = [
        'pk',
        'person',
        'date',
        'amount',
        'bookable',
        'purpose',
    ]

    def add_arguments(self, parser):
        today = date.today()

        parser.add_argument('--year', '-y', type=int, default=today.year)
        parser.add_argument('--month', '-m', type=int, default=today.month)

        parser.add_argument('--create', '-c', action='store_true')
        parser.add_argument('--book', '-b', action='store_true')
        parser.add_argument('--clear', '-C', action='store_true')

    def echo_queryset(self, queryset):
        echo(queryset_to_prettytable(queryset, self.HIBISCUS_TURNOVER_FIELDS,
                                     numbered=True),
             '', indent=2)

    def create(self, period):
        debts = MembershipFeeDebt.objects.create_for(period)

        for debt in debts:
            echo(red(debt))

        if debts:
            echo()

            if not confirmation_prompt('Apply?', default=True):
                raise CommandError('User Abort')

    def clear(self, period):
        account_donations = Account.objects.get_or_create(name='donations')[0]

        debts = MembershipFeeDebt.objects.filter(
            period__year=period.year,
            period__month=period.month,
        )

        if confirmation_prompt('Clear Donations?', default=True):
            for debt in debts:
                for booking in debt.bookings.all():
                    if booking.turnover:
                        booking.turnover.bookings.filter(
                            account=account_donations
                        ).delete()

        if confirmation_prompt('Clear Debts?', default=True):
            debts.delete()

    def search_turnover(self, debt):
        base_queryset = HibiscusTurnover.objects.filter(
            person=debt.person,
            bookable__gte=debt.fee,
        )

        value = option_prompt('  Search in (Month/Year/All)/Skip?', 'myas')

        while True:
            if value == 's':
                return None

            if value == 'a':
                queryset = base_queryset

            if value == 'y':
                queryset = base_queryset.filter(
                    date__year=debt.period.year,
                )

            elif value == 'm':
                queryset = base_queryset.filter(
                    date__year=debt.period.year,
                    date__month=debt.period.month,
                )

            elif value == 'c':
                value = range_prompt('  Turnover',
                                     range(1, queryset.count() + 1))

                return queryset[value - 1]

            self.echo_queryset(queryset)

            value = option_prompt('  Search in (Month/Year/All)/Choose/Skip?',
                                  'myacs')

    def book_on_turnover(self, debt, turnover):
        account_fees = Account.objects.get_or_create(name='membership fees')[0]
        account_donations = Account.objects.get_or_create(name='donations')[0]

        booking = turnover.book(account_fees, debt.fee)

        debt.bookings.add(booking)
        debt.save()

        echo('Booked {} on {}'.format(
            blue(booking),
            green(turnover),
        ), indent=2)

        # donations
        turnover = HibiscusTurnover.objects.get(pk=turnover.pk)

        if turnover.bookable > 0:
            echo()

            if confirmation_prompt('  Book remaining on donations?',
                                   default=True):

                donation = turnover.book(account_donations,
                                         turnover.bookable)

                echo('{} created'.format(green(donation)), indent=2)

    def book(self, period):
        for debt in MembershipFeeDebt.objects.filter(period=period,
                                                     paid=False):
            echo(red(debt))

            # search for turnover in self period
            qs = HibiscusTurnover.objects.filter(
                person=debt.person,
                date__year=period.year,
                date__month=period.month,
                bookable__gte=debt.fee,
            )

            if qs.count() == 1:
                self.echo_queryset(qs)

                value = option_prompt('  Book/Search Turnover',
                                      'Bs', default='B')

                if value == 'B':
                    turnover = qs.first()
                    self.book_on_turnover(debt, turnover)

                    echo()

                    continue

            # user search
            turnover = self.search_turnover(debt)

            if turnover:
                self.book_on_turnover(debt, turnover)

            echo()

        if not confirmation_prompt('Apply?'):
            raise CommandError('User Abort')

    @transaction.atomic
    def handle(self, *args, **options):
        period = date(options['year'], options['month'], 1)

        try:
            if options['create']:
                self.create(period)

            elif options['book']:
                self.book(period)

            elif options['clear']:
                self.clear(period)

        except KeyboardInterrupt:
            raise CommandError('User Abort')
