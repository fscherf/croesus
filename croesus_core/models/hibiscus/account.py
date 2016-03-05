from django.db import models

__all__ = [
    'HibiscusAccount',
]


class HibiscusAccount(models.Model):
    account_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    marking = models.CharField(max_length=100, blank=True, null=True)
    customer_number = models.CharField(max_length=25, blank=True, null=True)
    currency = models.CharField(max_length=5, blank=True, null=True)

    iban = models.CharField(max_length=30, blank=True, null=True)
    bic = models.CharField(max_length=11, blank=True, null=True)
    account_number = models.CharField(max_length=15, blank=True, null=True)
    bank_code = models.CharField(max_length=9, blank=True, null=True)

    balance = models.FloatField(blank=True, null=True)
    balance_available = models.FloatField(blank=True, null=True)
    balance_date = models.DateField(blank=True, null=True)

    comment = models.TextField(blank=True, null=True)

    class Meta:
        app_label = 'croesus_core'
