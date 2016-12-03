from django.core.management.base import BaseCommand, CommandError
from django.db import transaction as db_transaction

from ...models import Person, MembershipFeeDebt, Transaction, Booking, Account

from ...utils.shell import (
    shell_filter,
    echo,
    red,
    green,
    confirmation_prompt,
    option_prompt,
    choose_interactive,
    magenta,
    blue,
)

from datetime import date


class Command(BaseCommand):
    def add_arguments(self, parser):
        today = date.today()

        parser.add_argument('--year', '-y', type=int, default=today.year)
        parser.add_argument('--month', '-m', type=int, default=today.month)

        parser.add_argument('--members', nargs='+', type=int)
        parser.add_argument('--select-members', action='store_true')

    def get_membership_fee_debt(self, member, period, indent=0):
        echo('Searching for {} for {}@{} ...'.format(
            red('MemberShipFeeDebt'), blue(member), blue(period)
        ), indent=indent)

        debt = MembershipFeeDebt.objects.filter(
            person=member,
            period__year=period.year,
            period__month=period.month,
        )

        if not debt.exists():
            debt = MembershipFeeDebt.objects.create_for(period, persons=member)

            echo('{} created'.format(red(debt)), indent=4)

        else:
            echo('{} found'.format(red(debt)), indent=4)

        return debt.first()

    def get_payment(self, debt):
        field_lookups = {
            'date__year': debt.period.year,
            'date__month': debt.period.month,
        }

        prompt = '    search in ({}onth/{}ear/{}ll) / {}kip / search {}nteractive'.format(  # NOQA
            magenta('M'), magenta('Y'), magenta('A'), magenta('S'),
            magenta('I'))

        while True:
            # prepare and show payment objects
            bookings = Booking.objects.filter(
                account=Account.objects.get_membership_fee_account(),
                transaction__person=debt.person,
                membershipfeedebt__isnull=True,
                **field_lookups
            )

            transactions = Transaction.objects.filter(
                person=debt.person,
                bookable__gte=debt.fee,
                **field_lookups
            )

            if bookings.exists():
                echo('', green('Bookings'), bookings.to_prettytable(),
                     indent=4)

            if transactions.exists():
                echo('', green('Transactions'),
                     transactions.to_prettytable(
                         number_offset=bookings.count()),
                     indent=4)

            echo()

            payment_objects = list(bookings) + list(transactions)

            # handle user input
            value = option_prompt(prompt, 'myasi',
                                  range(0, len(payment_objects)))

            if type(value) == int:  # choose
                return payment_objects[value]

            elif value == 'm':  # month
                field_lookups = {
                    'date__year': debt.period.year,
                    'date__month': debt.period.month,
                }

            elif value == 'y':  # year
                field_lookups = {
                    'date__year': debt.period.year,
                }

            elif value == 'a':  # all
                field_lookups = {}

            elif value == 'i':  # interactive
                return choose_interactive([
                    ('croesus_core', 'Transaction'),
                    ('croesus_core', 'Booking'),
                ])

            elif value == 's':  # skip
                return None

    def ask_for_donation(self, transaction, period):
        if transaction.is_booked():
            return

        prompt = '    Donate remaining ({})?'.format(
            transaction.get_bookable())

        if confirmation_prompt(prompt):
            transaction.donate(date=period)

    @db_transaction.atomic
    def handle(self, *args, **options):
        period = date(options['year'], options['month'], 1)

        # members
        members = Person.objects.filter(member=True)

        if options['members']:
            members = members.filter(pk__in=options['members'])

        elif options['select_members']:
            members = shell_filter(members)

        # loop
        try:
            for member in members:
                echo('', magenta(member))

                # get/create debt
                debt = self.get_membership_fee_debt(member, period, indent=4)

                if not debt or debt.paid:
                    continue

                # pay debt
                payment = self.get_payment(debt)

                if not payment:
                    continue

                booking = debt.pay(payment)

                echo('paid with {}.bookings.{}'.format(
                    green(repr(booking.transaction)), green(repr(booking)),
                ), indent=4)

                # donate remaining
                if type(payment) == Transaction:
                    self.ask_for_donation(payment, period)

        except (KeyboardInterrupt, EOFError):
            raise CommandError('User Abort')

        # commit confirmation
        echo()

        try:
            if confirmation_prompt('Apply?'):
                return 0

        except (KeyboardInterrupt, EOFError):
            pass

        raise CommandError('User Abort')
