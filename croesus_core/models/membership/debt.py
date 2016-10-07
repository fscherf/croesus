from collections import Iterable

from django.db.models import BooleanField, Case, When, Sum, F
from django.db import transaction
from django.apps import apps
from django.db import models

from ...exceptions.membership_fee_debt import (
    MultipleMembershipFeeDebtsError,
)

__all__ = [
    'MembershipFeeDebt',
]


class MembershipFeeDebtQuerySet(models.QuerySet):
    pass


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

    @transaction.atomic
    def create_for(self, periods, persons=None):
        Person = apps.get_model('croesus_core', 'Person')

        if not persons:
            persons = Person.objects.filter(member=True)

        elif not isinstance(persons, Iterable):
            persons = [persons]

        if not isinstance(periods, Iterable):
            periods = [periods]

        for person in persons:
            for period in periods:
                agreement = person.get_membership_fee_agreement(period)

                if agreement:
                    debts = self.filter(person=person, period=period)

                    if debts.count() > 1:
                        raise MultipleMembershipFeeDebtsError(person=person,
                                                              period=period)

                    if not debts.exists():
                        self.create(
                            person=person,
                            period=period,
                            agreement=agreement,
                            fee=agreement.fee,
                        )

                    else:
                        debt = debts.first()

                        debt.fee = agreement.fee
                        debt.save()


class MembershipFeeDebt(models.Model):
    objects = MembershipFeeDebtManager()

    person = models.ForeignKey('croesus_core.Person')
    period = models.DateField()

    agreement = models.ForeignKey('croesus_core.MembershipFeeAgreement',
                                  blank=True, null=True)

    fee = models.FloatField()
    bookings = models.ManyToManyField('croesus_core.Booking')

    comment = models.TextField(blank=True, null=True, verbose_name='Comment')

    def __str__(self):
        return '<MembershipFeeDebt {}, {}, {}>'.format(self.person, self.period, self.fee)  # NOQA

    class Meta:
        app_label = 'croesus_core'
        unique_together = ('person', 'period', )
