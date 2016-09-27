from django.db.models import BooleanField, Case, When, Sum, F
from django.apps import apps
from django.db import models

__all__ = [
    'HibiscusTurnover',
]


class HibiscusTurnoverQuerySet(models.QuerySet):
    def match_ibans(self):
        for turnover in self.iterator():
            turnover.match_iban()


class HibiscusTurnoverManager(models.Manager):
    def get_queryset(self):
        return HibiscusTurnoverQuerySet(
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
        )


class HibiscusTurnover(models.Model):
    objects = HibiscusTurnoverManager()

    account_id = models.IntegerField(verbose_name='Account Id')
    turnover_id = models.IntegerField(verbose_name='Turnover Id')
    type = models.TextField(blank=True, null=True, verbose_name='Type')
    balance = models.FloatField(blank=True, null=True, verbose_name='Balance')
    amount = models.FloatField(blank=True, null=True, verbose_name='Amount')
    date = models.DateField(blank=True, null=True, verbose_name='Date')

    name = models.CharField(max_length=100, blank=True, null=True,
                            verbose_name='Name')
    customer_ref = models.TextField(blank=True, null=True,
                                    verbose_name='Customer Ref')
    iban = models.CharField(max_length=30, blank=True, null=True,
                            verbose_name='IBAN')
    bic = models.CharField(max_length=11, blank=True, null=True,
                           verbose_name='BIC')
    purpose = models.TextField(blank=True, null=True, verbose_name='Purpose')
    comment = models.TextField(blank=True, null=True, verbose_name='Comment')

    commercial_transaction_code = models.PositiveIntegerField(
        blank=True, null=True, verbose_name='Commercial Transaction Code')
    primanota = models.PositiveIntegerField(blank=True, null=True,
                                            verbose_name='Primanota')
    value_date = models.DateField(blank=True, null=True)

    person = models.ForeignKey('croesus_core.Person', blank=True, null=True,
                               verbose_name='Person')

    def book(self, account, amount):
        Booking = apps.get_model('croesus_core', 'Booking')

        return Booking.objects.create(
            turnover=self,
            account=account,
            amount=amount,
        )

    def match_iban(self):
        PersonAccount = apps.get_model('croesus_core', 'PersonAccount')

        if not self.iban:
            return

        pa = PersonAccount.objects.filter(iban=self.iban)

        if pa.count() == 1:
            self.person = pa[0].person
            self.save()

    class Meta:
        app_label = 'croesus_core'
        unique_together = ('account_id', 'turnover_id', )
        ordering = ['account_id', 'turnover_id']
