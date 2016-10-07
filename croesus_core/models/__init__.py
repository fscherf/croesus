from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver

from .accounting import *  # NOQA
from .membership import *  # NOQA
from .hibiscus import *  # NOQA
from .person import *  # NOQA

from ..utils.iban import compact, is_valid


@receiver(pre_save, sender=HibiscusAccount)  # NOQA
@receiver(pre_save, sender=HibiscusTurnover)  # NOQA
@receiver(pre_save, sender=PersonAccount)  # NOQA
def compact_ibans(sender, instance, **kwargs):
    if instance.iban:
        instance.iban = compact(instance.iban)

        valid, message = is_valid(instance.iban)

        if not valid:
            raise ValueError(message)


@receiver(pre_delete, sender=MembershipFeeDebt)  # NOQA
def delete_orphaned_bookings(sender, instance, **kwargs):
    instance.bookings.all().delete()
