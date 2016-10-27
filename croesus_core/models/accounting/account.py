from django.db import models

from ... import settings

__all__ = [
    'Account',
]


class AccountManager(models.Manager):
    def get_donation_account(self):
        return self.get_or_create(name=settings.DONATION_ACCOUNT_NAME)[0]

    def get_membership_fee_account(self):
        return self.get_or_create(name=settings.MEMBERSHIPFEE_ACCOUNT_NAME)[0]


class Account(models.Model):
    objects = AccountManager()

    name = models.CharField(max_length=50, verbose_name='Name', unique=True)
    comment = models.TextField(blank=True, null=True, verbose_name='Comment')

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'croesus_core'
