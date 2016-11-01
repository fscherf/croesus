from django.contrib import admin

from ..models import (
    MembershipFeeDebt,
    HibiscusTurnover,
    Account,
    Person,
)

from .accounting.account import AccountAdmin
from .membership.debt import MembershipFeeDebtAdmin
from .hibiscus.turnover import HibiscusTurnoverAdmin
from .person.person import PersonAdmin

admin.site.register(MembershipFeeDebt, MembershipFeeDebtAdmin)
admin.site.register(HibiscusTurnover, HibiscusTurnoverAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Person, PersonAdmin)
