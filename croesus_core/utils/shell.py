from prettytable import PrettyTable
from django.core.exceptions import FieldDoesNotExist

TABLE_RIGHT_ALIGNED_FIELDS = (
    'AutoField',
    'BigIntegerField',
    'BooleanField',
    'DecimalField',
    'DurationField',
    'FloatField',
    'IntegerField',
    'NullBooleanField',
    'PositiveIntegerField',
    'PositiveSmallIntegerField',
    'SmallIntegerField',
    'TimeField',
    'DateField',
    'DateTimeField',
)


def echo(*texts, indent=0):
    for text in texts:
        for line in str(text).split('\n'):
            print('{}{}'.format(' ' * indent, line))

    if not texts:
        print()


def red(text):
    return '\033[1;31m{}\033[1;m'.format(text)


def green(text):
    return '\033[1;32m{}\033[1;m'.format(text)


def blue(text):
    return '\033[1;34m{}\033[1;m'.format(text)


def option_prompt(text, options, default=None, no_color=False):
    ps = '{} [{}] '.format(text, '/'.join(list(options)))

    try:
        while True:
            user_input = input(ps)

            if user_input:
                user_input = user_input[0]

            if user_input and user_input in options:
                return user_input

            if not user_input and default:
                return default

            if not no_color:
                ps = red(ps)

    except KeyboardInterrupt:
        print()

        raise


def range_prompt(text, option_range, default=None, no_color=False):
    ps = '{} [{}..{}] '.format(text, option_range.start, option_range.stop - 1)

    try:
        while True:
            user_input = input(ps)

            try:
                if not user_input and default:
                    return default

                user_input = int(user_input)

                if user_input in option_range:
                    return user_input

            except ValueError:
                pass

            if not no_color:
                ps = red(ps)

    except KeyboardInterrupt:
        print()

        raise


def confirmation_prompt(text, default=None, no_color=False):
    ps = '{} [{}/{}] '.format(
        text,
        'Y' if default else 'y',
        'N' if type(default) == bool and not default else 'n'
    )

    try:
        while True:
            user_input = input(ps)

            if not user_input and type(default) == bool:
                return default

            if user_input and user_input[0] in 'yn':
                return {
                    'y': True,
                    'n': False,
                }[user_input[0]]

            if not no_color:
                ps = red(ps)

    except KeyboardInterrupt:
        print()

        raise


def queryset_to_prettytable(queryset, field_names=None, numbered=False):
    if not field_names:
        field_names = [i.name for i in queryset.model._meta.fields]

    table = PrettyTable()

    if numbered:
        table.field_names = ['#'] + field_names
        table.align['#'] = 'r'

    else:
        table.field_names = field_names

    table.align = 'l'

    for field_name in field_names:
        try:
            field = queryset.model._meta.get_field(field_name)

            if field.get_internal_type() in TABLE_RIGHT_ALIGNED_FIELDS:
                table.align[field_name] = 'r'

        except FieldDoesNotExist:
            pass

    for index, obj in enumerate(queryset):
        row = []

        for field_name in field_names:
            row.append(getattr(obj, field_name, '') or '')

        if numbered:
            row = [index + 1] + row

        table.add_row(row)

    return table
