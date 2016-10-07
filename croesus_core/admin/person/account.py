from django.contrib import admin


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
