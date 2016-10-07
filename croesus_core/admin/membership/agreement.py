from django.contrib import admin

from ...forms import MembershipFeeAgreementForm


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
