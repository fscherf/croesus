from django.db.models import Max, Min
from django.contrib import admin


class StatementAdmin(admin.ModelAdmin):
    list_display = (
        'file_name',
        'created',
        'transaction_min_date',
        'transaction_max_date',
    )

    def transaction_min_date(self, obj):
        return obj.transaction_set.aggregate(Min('date'))['date__min']

    def transaction_max_date(self, obj):
        return obj.transaction_set.aggregate(Max('date'))['date__max']
