from django.core.urlresolvers import reverse
from django.utils.html import mark_safe
from django.contrib import admin
from django.apps import apps

from ..list_filter import YearFilter, MonthFilter, BooleanFilter
from ...models import Booking


class TransactionTypeFilter(admin.SimpleListFilter):
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


class TransactionYearFilter(YearFilter):
    title = 'Year'
    parameter_name = 'date__year'


class TransactionMonthFilter(MonthFilter):
    title = 'Month'
    parameter_name = 'date__month'


class TransactionUnderbookedFilter(BooleanFilter):
    title = 'Underbooked'
    parameter_name = 'underbooked'


class TransactionBookedFilter(BooleanFilter):
    title = 'Booked'
    parameter_name = 'booked'


class TransactionOverbookedFilter(BooleanFilter):
    title = 'Overbooked'
    parameter_name = 'overbooked'


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


class TransactionAdmin(admin.ModelAdmin):
    change_list_template = 'croesus_core/admin/bank/transaction/change_list.html'  # NOQA
    ordering = ['-date']

    inlines = [
        BookingInline,
    ]

    list_filter = (
        TransactionTypeFilter,
        TransactionYearFilter,
        TransactionMonthFilter,
        TransactionUnderbookedFilter,
        TransactionBookedFilter,
        TransactionOverbookedFilter,
        PersonTypeFilter,
        'person',
    )

    # list_display
    list_display = (
        'colored_amount',
        'date',
        'person_link',
        'purpose',
        'bookings_amount',
        'bookable',
        'underbooked',
        'booked',
        'overbooked',
    )

    def colored_amount(self, obj):
        template = '<span style="color: {};">{:+.2f}</span>'
        color = 'limegreen' if obj.amount >= 0 else 'red'

        return mark_safe(template.format(color, obj.amount))

    colored_amount.short_description = 'Amount'

    def person_link(self, obj):
        if obj.person:
            return mark_safe('<a href="{}">{}</a>'.format(
                reverse('admin:croesus_core_person_change',
                        args=[obj.person.pk]),
                str(obj.person),
            ))

        if obj.name:
            return obj.name

        return ''

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
