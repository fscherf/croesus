from django import template

register = template.Library()


@register.filter
def mediawiki_number(number):
    return str(number).replace('.', ',')


@register.filter
def mediawiki_month(number):
    return ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli',
            'August', 'September', 'Oktober', 'November',
            'Dezember'][number - 1]


@register.filter
def strftime(value, format):
    return value.strftime(format)
