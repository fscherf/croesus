from django.contrib import admin

from ...models import MembershipFeeAgreement, PersonInactiveRule
from ...forms import PersonForm, MembershipFeeAgreementForm


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
