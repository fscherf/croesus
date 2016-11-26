from django.contrib import admin

from ..models import (
    MembershipFeeDebt,
    Transaction,
    Statement,
    Account,
    Person,
)

from .accounting.account import AccountAdmin
from .membership.debt import MembershipFeeDebtAdmin
from .bank.transaction import TransactionAdmin
from .bank.statement import StatementAdmin
from .person.person import PersonAdmin

admin.site.register(MembershipFeeDebt, MembershipFeeDebtAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Statement, StatementAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Person, PersonAdmin)
