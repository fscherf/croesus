from django.contrib import admin

from ...models import MembershipFeeAgreement, PersonInactiveRule
from ...forms import PersonForm


class MembershipFeeAgreementInline(admin.TabularInline):
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
