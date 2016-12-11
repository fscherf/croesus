from django.db.models import Sum, F, When, Case, BooleanField, FloatField
from django.db import models, transaction as db_transaction
from django.apps import apps

from ...utils.mt940 import parse_mt940, parse_mt940_transaction_details
from ..base import CroesusQueryset

__all__ = [
    'Transaction',
]


class TransactionQuerySet(CroesusQueryset):
    PRETTYTABLE_FIELDS = [
        'pk',
        'amount',
        'date',
        'person',
        'purpose',
        'bookings_amount',
        'bookable',
    ]

    def match_ibans(self):
        for transaction in self.iterator():
            transaction.match_iban()


class TransactionManager(models.Manager):
    def get_queryset(self):
        return TransactionQuerySet(
            self.model,
            using=self._db,
        ).annotate(
            bookings_amount=Sum('bookings__amount'),
        ).annotate(
            underbooked=Case(
                When(bookings_amount__isnull=True, then=True),
                When(bookings_amount__lt=F('amount'), then=True),
                output_field=BooleanField(),
                default=False,
            ),
            booked=Case(
                When(bookings_amount__gte=F('amount'), then=True),
                output_field=BooleanField(),
                default=False,
            ),
            overbooked=Case(
                When(bookings_amount__gt=F('amount'), then=True),
                output_field=BooleanField(),
                default=False,
            ),
            bookable=Case(
                When(bookings_amount__isnull=False,
                     then=F('amount') - F('bookings_amount')),
                output_field=FloatField(),
                default=F('amount'),
            ),
        )

    @db_transaction.atomic
    def parse_statement(self, statement, parse_details=True, match_ibans=True):
        dates = [i[0] for i in self.values_list('date')]
        objects = []

        mt940_transactions = parse_mt940(statement.data)

        bank_code, account_number =\
            mt940_transactions.data['account_identification'].split('/')

        for mt940_transaction in parse_mt940(statement.data):
            data = mt940_transaction.data

            # skip dataset if date is already known to the database
            # this is to avoid glitches
            if data['date'] in dates:
                continue

            final_opening_balance = data.get('final_opening_balance', None)
            final_closing_balance = data.get('final_closing_balance', None)

            if final_opening_balance:
                final_opening_balance = final_opening_balance.amount.amount

            if final_closing_balance:
                final_closing_balance = final_closing_balance.amount.amount

            objects.append(Transaction(
                statement=statement,
                bank_code=bank_code,
                account_number=account_number,
                date=data['date'],
                amount=float(data['amount'].amount),
                details=data['transaction_details'],
                currency=data['currency'],
                final_opening_balance=final_opening_balance,
                final_closing_balance=final_closing_balance,
            ))

        if objects:
            if parse_details or match_ibans:
                for obj in objects:
                    if parse_details:
                        obj.parse_details(save=False)

                    if match_ibans:
                        obj.match_iban(save=False)

            self.bulk_create(objects)

        return len(objects)


class Transaction(models.Model):
    objects = TransactionManager()

    # data
    statement = models.ForeignKey('croesus_core.Statement', blank=True,
                                  null=True, verbose_name='Statement')

    created = models.DateTimeField(auto_now_add=True, editable=False)

    # parsed data
    amount = models.FloatField(blank=True, null=True)
    currency = models.CharField(max_length=8, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    bank_code = models.CharField(max_length=16, blank=True, null=True)
    account_number = models.CharField(max_length=16, blank=True, null=True)
    details = models.TextField(blank=True, null=True)

    final_opening_balance = models.FloatField(blank=True, null=True)
    final_opening_balance_date = models.DateField(blank=True, null=True)

    final_closing_balance = models.FloatField(blank=True, null=True)
    final_closing_balance_date = models.DateField(blank=True, null=True)

    # data parsed from details
    name = models.CharField(max_length=128, blank=True, null=True)
    purpose = models.TextField(blank=True, null=True)

    iban = models.CharField(max_length=30, blank=True, null=True,
                            verbose_name='IBAN')

    bic = models.CharField(max_length=11, blank=True, null=True,
                           verbose_name='BIC')

    person = models.ForeignKey('croesus_core.Person', blank=True, null=True,
                               verbose_name='Person')

    # additional data
    comment = models.TextField(blank=True, null=True)

    def get_bookings_amount(self):
        return self.bookings.aggregate(Sum('amount'))['amount__sum'] or 0.0

    def get_bookable(self):
        bookings_amount = self.get_bookings_amount()

        if bookings_amount >= self.amount:
            return 0.0

        return self.amount - self.get_bookings_amount()

    def is_underbooked(self):
        return self.get_bookings_amount() < self.amount

    def is_booked(self):
        return self.get_bookings_amount() >= self.amount

    def is_overbooked(self):
        return self.get_bookings_amount() > self.amount

    def parse_details(self, save=True):
        details = parse_mt940_transaction_details(self.details,
                                                  bank_code=self.bank_code)

        for key, value in details.items():
            setattr(self, key, value)

        if save:
            self.save()

    def match_iban(self, save=True):
        PersonAccount = apps.get_model('croesus_core', 'PersonAccount')

        if not self.iban:
            return

        pa = PersonAccount.objects.filter(iban=self.iban)

        if pa.count() == 1:
            self.person = pa[0].person

            if save:
                self.save()

    def book(self, account, amount=None, date=None):
        Booking = apps.get_model('croesus_core', 'Booking')

        return Booking.objects.create(
            transaction=self,
            account=account,
            amount=amount or self.get_bookable(),
            date=date,
        )

    def donate(self, amount=None, date=None):
        Account = apps.get_model('croesus_core', 'Account')

        return self.book(
            account=Account.objects.get_donation_account(),
            amount=amount,
            date=date,
        )
