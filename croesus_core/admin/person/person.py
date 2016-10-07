from django.contrib import admin

from ...forms import PersonForm


class PersonAdmin(admin.ModelAdmin):
    form = PersonForm

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
