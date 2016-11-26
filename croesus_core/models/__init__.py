from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver

from .accounting import *  # NOQA
from .membership import *  # NOQA
from .person import *  # NOQA
from .bank import *  # NOQA

from ..utils.iban import compact, is_valid


@receiver(pre_save, sender=PersonAccount)  # NOQA
@receiver(pre_save, sender=Transaction)  # NOQA
def compact_ibans(sender, instance, **kwargs):
    if instance.iban:
        instance.iban = compact(instance.iban)

        valid, message = is_valid(instance.iban)

        if not valid and sender is not Transaction:  # NOQA
            # FIXME: There are IBANs of the SPARKASSE without an country code
            raise ValueError(message)


@receiver(pre_delete, sender=MembershipFeeDebt)  # NOQA
def delete_orphaned_bookings(sender, instance, **kwargs):
    instance.bookings.all().delete()
