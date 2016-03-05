from django.contrib import admin

from .forms import (
    PersonForm,
    MembershipFeeAgreementForm,
    MembershipFeeDebtForm,
)

from .models import (
    Person,
    PersonAccount,
    MembershipFeeAgreement,
    MembershipFeeDebt,
)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    form = PersonForm

    list_display = (
        'name',
        'surname',
        'nickname',
        'email_address',
        'type',
        'accession',
    )

    list_filter = (
        'type',
    )


@admin.register(PersonAccount)
class PersonAccountAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'person',
        'iban',
        'bic',
    )

    list_filter = (
        'person',
    )


@admin.register(MembershipFeeAgreement)
class MembershipFeeAgreementAdmin(admin.ModelAdmin):
    form = MembershipFeeAgreementForm

    list_display = (
        'person',
        'fee',
        'currency',
        'repayment_period_in_months',
        'start',
        'end',
    )

    list_filter = (
        'person',
    )


@admin.register(MembershipFeeDebt)
class MembershipFeeDebtAdmin(admin.ModelAdmin):
    form = MembershipFeeDebtForm

    list_display = (
        'person',
        'period',
        'fee',
    )

    list_filter = (
        'person',
        'period',
    )
