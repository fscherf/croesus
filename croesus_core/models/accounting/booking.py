from prettytable import PrettyTable, ALL, NONE

from django.db import models

from ..base import CroesusQueryset

__all__ = [
    'Booking',
]


class BookingQuerySet(CroesusQueryset):
    def to_prettytable(self, field_names=None, numbered=True,
                       number_offset=0):

        table = PrettyTable()
        field_names = ['Amount', 'Date', 'Account', 'Person', 'Coment']

        if numbered:
            field_names = ['#'] + field_names

        table.field_names = field_names
        table.align = 'l'
        table.vrules = NONE
        table.hrules = ALL
        table.horizontal_char = '─'

        if numbered:
            table.align['#'] = 'r'

        for index, booking in enumerate(self.iterator()):
            row = [
                booking.amount or '',
                booking.date or '',
                booking.account or '',
                booking.transaction.person if booking.transaction else '',
                booking.comment or '',
            ]

            if numbered:
                row.insert(0, index + number_offset)

            table.add_row(row)

        return table


class BookingManager(models.Manager):
    def get_queryset(self):
        return BookingQuerySet(self.model, using=self._db)


class Booking(models.Model):
    objects = BookingManager()

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
