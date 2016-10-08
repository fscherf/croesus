from django.db import models

__all__ = [
    'Booking',
]


class Booking(models.Model):
    amount = models.FloatField(verbose_name='Amount')
    date = models.DateTimeField(auto_now_add=True)

    account = models.ForeignKey(
        'croesus_core.Account',
        on_delete=models.PROTECT,
    )

    turnover = models.ForeignKey(
        'croesus_core.HibiscusTurnover',
        related_name='bookings',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )

    comment = models.TextField(blank=True, null=True, verbose_name='Comment')

    class Meta:
        app_label = 'croesus_core'
        ordering = ['date']

    def __str__(self):
        return '<Booking:{}, {}, {}>'.format(self.pk, self.amount,
                                             self.account)
