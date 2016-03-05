from django.db import models

__all__ = [
    'PersonInactiveRule',
]


class PersonInactiveRule(models.Model):
    person = models.ForeignKey('croesus_core.Person')
    start = models.DateField(verbose_name='Start')
    end = models.DateField(verbose_name='End', blank=True, null=True)

    comment = models.TextField(blank=True, null=True, verbose_name='Comment')

    class Meta:
        app_label = 'croesus_core'
        ordering = ['start']
