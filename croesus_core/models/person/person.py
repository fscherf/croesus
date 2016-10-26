from dateutil.relativedelta import relativedelta

from django.db.models import Case, When, Q, BooleanField
from django.db import models

from ...utils.serializers import PrettyYamlSerializer

from ...exceptions.membership_fee_agreement import (
    MultipleMembershipFeeAgreementsError,
)

__all__ = [
    'Person',
]


class PersonQuerySet(models.QuerySet):
    def dump(self, buffer):
        for index, person in enumerate(self.order_by('surname', 'name')):
            if index > 0:
                buffer.write('\n')

            person.dump(buffer)


class PersonManager(models.Manager):
    def get_queryset(self):
        return PersonQuerySet(
            self.model,
            using=self._db,
        ).annotate(
            member=Case(
                When(type=Person.MEMBER, then=True),
                output_field=BooleanField(),
                default=False,
            ),
            legal_person=Case(
                When(type=Person.LEGAL_PERSON, then=True),
                output_field=BooleanField(),
                default=False,
            ),
        )


class Person(models.Model):
    MEMBER = 'm'
    LEGAL_PERSON = 'l'

    objects = PersonManager()

    type = models.CharField(max_length=1, verbose_name='Type')
    name = models.CharField(max_length=50, verbose_name='Name')
    surname = models.CharField(max_length=50, blank=True, null=True,
                               verbose_name='Surname')
    nickname = models.CharField(max_length=50, blank=True, null=True,
                                verbose_name='Nickname')
    email_address = models.EmailField(unique=True, blank=True, null=True,
                                      verbose_name='Email address')
    accession = models.DateField(verbose_name='Accession', blank=True,
                                 null=True)

    comment = models.TextField(blank=True, null=True, verbose_name='Comment')

    def __str__(self):
        return '{}{}{}'.format(
           self.name, ' ' + self.surname if self.surname else '',
           ' ({})'.format(self.nickname) if self.nickname else '')

    def clean(self):
        if not self.email_address:
            self.email_address = None

    def get_membership_fee_agreement(self, period):
        # only members can pay membership fees
        if self.type != self.MEMBER:
            return None

        # check for inactive rules
        inactive_rules = self.personinactiverule_set.filter(
            Q(end__isnull=True) | Q(end__gt=period),
            start__lte=period,
        )

        if inactive_rules.exists():
            return None

        # agreement
        agreements = self.membershipfeeagreement_set.filter(
            Q(end__isnull=True) | Q(end__gt=period),
            start__lte=period,
        )

        if agreements.count() < 1:
            return None

        if agreements.count() > 1:
            raise MultipleMembershipFeeAgreementsError(agreements)

        agreement = agreements.first()

        # calculate repayment period
        rdelta = relativedelta(period, agreement.start)

        if((rdelta.months + agreement.repayment_period_in_months) %
           agreement.repayment_period_in_months == 0):
            return agreement

        return None

    def dump(self, buffer):
        def write_title(title, line_length=80):
            buffer.write('# {} {}\n'.format(
                title,
                '#' * (line_length - len(title) - 4)))

        serializer = PrettyYamlSerializer()

        # Person
        write_title(str(self))
        serializer.serialize([self], stream=buffer)
        buffer.write('\n')

        # PersonAccounts
        if self.personaccount_set.count() > 0:
            write_title('PersonAccounts', line_length=60)

            serializer.serialize(
                self.personaccount_set.all().order_by('iban'), stream=buffer)

            buffer.write('\n')

        # MembershipFeeAgreements
        if self.membershipfeeagreement_set.count() > 0:
            write_title('MembershipFeeAgreements', line_length=60)

            serializer.serialize(
                self.membershipfeeagreement_set.all().order_by('start'),
                stream=buffer,
            )

            buffer.write('\n')

        # InactiveRules
        if self.personinactiverule_set.count() > 0:
            write_title('InactiveRules', line_length=60)

            serializer.serialize(
                self.personinactiverule_set.all().order_by('start'),
                stream=buffer,
            )

            buffer.write('\n')

    class Meta:
        app_label = 'croesus_core'
