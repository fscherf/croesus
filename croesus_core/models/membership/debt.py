from prettytable import PrettyTable, ALL, NONE
from collections import Iterable

from django.db.models import BooleanField, Case, When, Sum, F
from django.db import transaction as db_transaction
from django.apps import apps
from django.db import models

from ...exceptions.membership_fee_debt import (
    MultipleMembershipFeeDebtsError,
)

from ..base import CroesusQueryset

__all__ = [
    'MembershipFeeDebt',
]


class MembershipFeeDebtQuerySet(CroesusQueryset):
    def to_prettytable(self, field_names=None, numbered=True,
                       number_offset=0):

        table = PrettyTable()
        field_names = ['Person', 'Period', 'Fee', 'Agreement', 'Unpaid',
                       'Paid', 'Overpaid', 'Comment']

        if numbered:
            field_names = ['#'] + field_names

        table.field_names = field_names
        table.align = 'l'
        table.vrules = NONE
        table.hrules = ALL
        table.horizontal_char = '─'

        if numbered:
            table.align['#'] = 'r'

        table.align['Fee'] = 'r'
        table.align['Unpaid'] = 'r'
        table.align['Paid'] = 'r'
        table.align['Overpaid'] = 'r'

        for index, debt in enumerate(self.iterator()):
            row = [
                debt.person,
                debt.period,
                debt.fee,
                debt.agreement,
                'x' if debt.unpaid else '',
                'x' if debt.paid else '',
                'x' if debt.overpaid else '',
                debt.comment or '',
            ]

            if numbered:
                row.insert(0, index + number_offset)

            table.add_row(row)

        return table


class MembershipFeeDebtManager(models.Manager):
    def get_queryset(self):
        return MembershipFeeDebtQuerySet(
            self.model,
            using=self._db,
        ).annotate(
            bookings_amount=Sum('bookings__amount'),
        ).annotate(
            unpaid=Case(
                When(bookings_amount__isnull=True, then=True),
                When(bookings_amount__lt=F('fee'), then=True),
                output_field=BooleanField(),
                default=False,
            ),
            paid=Case(
                When(bookings_amount__gte=F('fee'), then=True),
                output_field=BooleanField(),
                default=False,
            ),
            overpaid=Case(
                When(bookings_amount__gt=F('fee'), then=True),
                output_field=BooleanField(),
                default=False,
            ),
        )

    @db_transaction.atomic
    def create_for(self, periods, persons=None):
        Person = apps.get_model('croesus_core', 'Person')

        if not persons:
            persons = Person.objects.filter(member=True)

        elif not isinstance(persons, Iterable):
            persons = [persons]

        if not isinstance(periods, Iterable):
            periods = [periods]

        debt_pks = []

        for person in persons:
            for period in periods:
                agreement = person.get_membership_fee_agreement(period)

                if agreement:
                    debts = self.filter(person=person, period=period)

                    if debts.count() > 1:
                        raise MultipleMembershipFeeDebtsError(person=person,
                                                              period=period)

                    if not debts.exists():
                        debt = self.create(
                            person=person,
                            period=period,
                            agreement=agreement,
                            fee=agreement.fee,
                        )

                        debt_pks.append(debt.pk)

        return self.filter(pk__in=debt_pks)


class MembershipFeeDebt(models.Model):
    objects = MembershipFeeDebtManager()

    person = models.ForeignKey('croesus_core.Person')
    period = models.DateField()

    agreement = models.ForeignKey('croesus_core.MembershipFeeAgreement',
                                  blank=True, null=True)

    fee = models.FloatField()
    bookings = models.ManyToManyField('croesus_core.Booking')

    comment = models.TextField(blank=True, null=True, verbose_name='Comment')

    @db_transaction.atomic
    def pay(self, model_object):
        Transaction = apps.get_model('croesus_core', 'Transaction')
        Account = apps.get_model('croesus_core', 'Account')
        Booking = apps.get_model('croesus_core', 'Booking')

        if not type(model_object) in (Transaction, Booking):
            raise ValueError  # FIXME

        if type(model_object) == Transaction:
            booking = model_object.book(
                account=Account.objects.get_membership_fee_account(),
                amount=self.fee,
                date=self.period,
            )

        else:
            booking = model_object

        self.bookings.add(booking)
        self.save()

        return booking

    def __str__(self):
        return '<MembershipFeeDebt {}, {}, {}>'.format(self.person, self.period, self.fee)  # NOQA

    class Meta:
        app_label = 'croesus_core'
        unique_together = ('person', 'period', )
