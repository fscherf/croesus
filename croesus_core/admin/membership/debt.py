from django.contrib import admin

from ...forms import MembershipFeeDebtForm
from ..list_filter import YearFilter, MonthFilter, BooleanFilter


class MembershipFeeDebtYearFilter(YearFilter):
    title = 'Year'
    parameter_name = 'period__year'


class MembershipFeeDebtMonthFilter(MonthFilter):
    title = 'Month'
    parameter_name = 'period__month'


class MembershipFeeDebtPaidFilter(BooleanFilter):
    title = 'Paid'
    parameter_name = 'paid'


class MembershipFeeDebtOverPaidFilter(BooleanFilter):
    title = 'Overpaid'
    parameter_name = 'overpaid'


class MembershipFeeDebtAdmin(admin.ModelAdmin):
    form = MembershipFeeDebtForm

    list_display = (
        'person',
        'period',
        'fee',
        'bookings_amount',
        'paid',
        'overpaid',
    )

    list_filter = (
        MembershipFeeDebtYearFilter,
        MembershipFeeDebtMonthFilter,
        MembershipFeeDebtPaidFilter,
        MembershipFeeDebtOverPaidFilter,
        'person',
    )

    def bookings_amount(self, obj):
        return obj.bookings_amount or 0.0

    bookings_amount.short_description = 'Bookings Amount'

    def paid(self, obj):
        return obj.paid

    paid.short_description = 'Paid'
    paid.boolean = True

    def overpaid(self, obj):
        return obj.overpaid

    overpaid.short_description = 'Overpaid'
    overpaid.boolean = True
