from django.contrib import admin


class BooleanFilter(admin.SimpleListFilter):
    def lookups(self, request, model_admin):
        return (
            ('true', 'True',),
            ('false', 'False',),
        )

    def queryset(self, request, queryset):
        value = self.value()

        if not value:
            return queryset

        value = {
            'true': True,
            'false': False,
        }.get(value.lower(), 'false')

        return queryset.filter(**{self.parameter_name: value})


class YearFilter(admin.SimpleListFilter):
    def lookups(self, request, model_admin):
        field = self.parameter_name.split('__')[0]

        for i in model_admin.get_queryset(request).dates(field, 'year'):
            yield i.year, i.year

    def queryset(self, request, queryset):
        value = self.value()

        if not value:
            return queryset

        value = int(self.value())

        return queryset.filter(**{self.parameter_name: value})


class MonthFilter(admin.SimpleListFilter):
    MONTH_NAMES = [
        'January',
        'February',
        'March',
        'April',
        'May',
        'June',
        'July',
        'August',
        'September',
        'October',
        'November',
        'December',
    ]

    def lookups(self, request, model_admin):
        field = self.parameter_name.split('__')[0]
        dates = model_admin.get_queryset(request).dates(field, 'month')
        months = set(sorted([i.month for i in dates]))

        for month in months:
            yield month, self.MONTH_NAMES[month - 1]

    def queryset(self, request, queryset):
        value = self.value()

        if not value:
            return queryset

        value = int(self.value())

        return queryset.filter(**{self.parameter_name: value})
