from django.utils.html import mark_safe
from django.contrib import admin

from ..list_filter import BooleanFilter, YearFilter, MonthFilter
from ...models import Booking


class HibiscusTurnoverUnderbookedFilter(BooleanFilter):
    title = 'Underbooked'
    parameter_name = 'underbooked'


class HibiscusTurnoverBookedFilter(BooleanFilter):
    title = 'Booked'
    parameter_name = 'booked'


class HibiscusTurnoverOverbookedFilter(BooleanFilter):
    title = 'Overbooked'
    parameter_name = 'overbooked'


class HibiscusTurnoverYearFilter(YearFilter):
    title = 'Year'
    parameter_name = 'date__year'


class HibiscusTurnoverMonthFilter(MonthFilter):
    title = 'Month'
    parameter_name = 'date__month'


class BookingInline(admin.TabularInline):
    model = Booking
    extra = 1


class HibiscusTurnoverAdmin(admin.ModelAdmin):
    ordering = ['-date']

    inlines = [
        BookingInline,
    ]

    list_display = (
        'colored_amount',
        'balance',
        'date',
        'person',
        'purpose',
        'bookings_amount',
        'bookable',
        'underbooked',
        'booked',
        'overbooked',
    )

    list_filter = (
        HibiscusTurnoverYearFilter,
        HibiscusTurnoverMonthFilter,
        HibiscusTurnoverUnderbookedFilter,
        HibiscusTurnoverBookedFilter,
        HibiscusTurnoverOverbookedFilter,
        'person',
    )

    def colored_amount(self, obj):
        template = '<span style="color: {};">{:+.2f}</span>'
        color = 'limegreen' if obj.amount >= 0 else 'red'

        return mark_safe(template.format(color, obj.amount))

    colored_amount.short_description = 'Amount'

    def bookings_amount(self, obj):
        return obj.bookings_amount or 0.0

    bookings_amount.short_description = 'Bookings Amount'

    def underbooked(self, obj):
        return obj.underbooked

    underbooked.short_description = 'Underbooked'
    underbooked.boolean = True

    def booked(self, obj):
        return obj.booked

    booked.short_description = 'Booked'
    booked.boolean = True

    def overbooked(self, obj):
        return obj.overbooked

    overbooked.short_description = 'Overbooked'
    overbooked.boolean = True

    def bookable(self, obj):
        return obj.bookable
