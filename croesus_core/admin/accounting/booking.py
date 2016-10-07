from django.contrib import admin


class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'amount',
        'date',
        'account',
    )

    list_filter = (
        'account',
    )
