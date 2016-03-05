from django.db import models

__all__ = [
    'PersonAccount',
]


class PersonAccount(models.Model):
    person = models.ForeignKey('croesus_core.Person')

    name = models.CharField(max_length=100, blank=True, null=True)
    iban = models.CharField(max_length=30, unique=True)
    bic = models.CharField(max_length=11)

    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return '{}: IBAN: {}, BIC: {}'.format(self.person, self.iban, self.bic)

    class Meta:
        app_label = 'croesus_core'
