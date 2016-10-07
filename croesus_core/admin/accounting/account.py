from django.contrib import admin


class AccountAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )
