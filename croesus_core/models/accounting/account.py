from django.db import models

__all__ = [
    'Account',
]


class Account(models.Model):
    name = models.CharField(max_length=50, verbose_name='Name', unique=True)
    comment = models.TextField(blank=True, null=True, verbose_name='Comment')

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'croesus_core'
