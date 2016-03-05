from django.db import models

__all__ = [
    'MembershipFeeAgreement',
]


class MembershipFeeAgreement(models.Model):
    person = models.ForeignKey('croesus_core.Person')

    fee = models.FloatField(verbose_name='Fee')
    repayment_period_in_months = models.IntegerField(
        verbose_name='Repayment Period In Months')
    currency = models.CharField(max_length=5, verbose_name='Currency')

    start = models.DateField(verbose_name='Start')
    end = models.DateField(verbose_name='End', blank=True, null=True)

    comment = models.TextField(blank=True, null=True, verbose_name='Comment')

    def __str__(self):
        return '{} {}{} ({} - {})'.format(
            str(self.person),
            str(self.fee),
            str(self.currency),
            str(self.start),
            str(self.end))

    class Meta:
        app_label = 'croesus_core'
        ordering = ['start']
