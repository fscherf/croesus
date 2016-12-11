from django.db import models

__all__ = [
    'Booking',
]


class Booking(models.Model):
    amount = models.FloatField(verbose_name='Amount')
    date = models.DateField(blank=True, null=True)

    account = models.ForeignKey(
        'croesus_core.Account',
        on_delete=models.PROTECT,
    )

    transaction = models.ForeignKey(
        'croesus_core.Transaction',
        related_name='bookings',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )

    comment = models.TextField(blank=True, null=True, verbose_name='Comment')
    booked = models.DateField(auto_now_add=True, editable=False, null=True,
                              blank=True)

    class Meta:
        app_label = 'croesus_core'
        ordering = ['date']

    def __str__(self):
        return '{}, {}, {}'.format(self.pk, self.amount, self.account)
