from django.contrib import admin

from ..models import (
    MembershipFeeAgreement,
    PersonInactiveRule,
    MembershipFeeDebt,
    HibiscusTurnover,
    PersonAccount,
    Account,
    Booking,
    Person,
)

from .accounting.account import AccountAdmin
from .accounting.booking import BookingAdmin
from .membership.agreement import MembershipFeeAgreementAdmin
from .membership.debt import MembershipFeeDebtAdmin
from .hibiscus.turnover import HibiscusTurnoverAdmin
from .person.person import PersonAdmin
from .person.account import PersonAccountAdmin

admin.site.register(MembershipFeeAgreement, MembershipFeeAgreementAdmin)
admin.site.register(MembershipFeeDebt, MembershipFeeDebtAdmin)
admin.site.register(HibiscusTurnover, HibiscusTurnoverAdmin)
admin.site.register(PersonAccount, PersonAccountAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(PersonInactiveRule)
