from django.contrib import admin

from ...models import PersonAccount, MembershipFeeAgreement, PersonInactiveRule
from ...forms import PersonForm, MembershipFeeAgreementForm


class PersonAccountInline(admin.TabularInline):
    model = PersonAccount
    extra = 1


class MembershipFeeAgreementInline(admin.TabularInline):
    form = MembershipFeeAgreementForm
    model = MembershipFeeAgreement
    extra = 1


class PersonInactiveRuleInline(admin.TabularInline):
    model = PersonInactiveRule
    extra = 1


class PersonAdmin(admin.ModelAdmin):
    form = PersonForm

    inlines = [
        PersonAccountInline,
        MembershipFeeAgreementInline,
        PersonInactiveRuleInline,
    ]

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
