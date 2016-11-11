from django.core.urlresolvers import reverse
from django.utils.html import mark_safe
from django.contrib import admin
from django.apps import apps

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


class HibiscusTurnoverTypeFilter(admin.SimpleListFilter):
    title = 'Type'
    parameter_name = 'type'

    def queryset(self, request, queryset):
        value = self.value()

        if value == 'r':
            return queryset.filter(amount__gt=0)

        if value == 'e':
            return queryset.filter(amount__lt=0)

        return queryset

    def lookups(self, request, model_admin):
        return (
            ('r', 'Receipt',),
            ('e', 'Expenditure',),
        )


class PersonTypeFilter(admin.SimpleListFilter):
    title = 'Person Type'
    parameter_name = 'person__type'

    def queryset(self, request, queryset):
        value = self.value()

        if not value:
            return queryset

        return queryset.filter(person__type=self.value())

    def lookups(self, request, model_admin):
        Person = apps.get_model('croesus_core', 'Person')

        return (
            (Person.MEMBER, 'Member',),
            (Person.LEGAL_PERSON, 'Legal Person',),
        )


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
        'colored_balance',
        'date',
        'person_link',
        'purpose',
        'bookings_amount',
        'bookable',
        'underbooked',
        'booked',
        'overbooked',
    )

    search_fields = (
        'type',
        'balance',
        'amount',
        'name',
        'customer_ref',
        'iban',
        'bic',
        'purpose',
        'comment',
        'commercial_transaction_code',
    )

    list_filter = (
        HibiscusTurnoverTypeFilter,
        HibiscusTurnoverYearFilter,
        HibiscusTurnoverMonthFilter,
        HibiscusTurnoverUnderbookedFilter,
        HibiscusTurnoverBookedFilter,
        HibiscusTurnoverOverbookedFilter,
        PersonTypeFilter,
        'person',
    )

    def colored_amount(self, obj):
        template = '<span style="color: {};">{:+.2f}</span>'
        color = 'limegreen' if obj.amount >= 0 else 'red'

        return mark_safe(template.format(color, obj.amount))

    colored_amount.short_description = 'Amount'

    def colored_balance(self, obj):
        if obj.balance >= 0:
            return obj.balance

        template = '<span style="color: red;">{:+.2f}</span>'

        return mark_safe(template.format(obj.balance))

    colored_balance.short_description = 'Balance'

    def person_link(self, obj):
        if not obj.person:
            return ''

        return mark_safe('<a href="{}">{}</a>'.format(
            reverse('admin:croesus_core_person_change', args=[obj.person.pk]),
            str(obj.person),
        ))

    person_link.short_description = 'Person'

    def bookings_amount(self, obj):
        return obj.bookings_amount or 0.0

    bookings_amount.short_description = 'Bookings Amount'

    def bookable(self, obj):
        return obj.bookable

    bookable.short_description = 'Bookable'

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
