from prettytable import PrettyTable
from django.core.exceptions import FieldDoesNotExist
import tempfile
from subprocess import call
from django.template.loader import render_to_string
import os
from IPython import embed
from django.apps import apps

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


def magenta(text):
    return '\033[1;36m{}\033[1;m'.format(text)


def option_prompt(text, options, option_range=None, default=None,
                  no_color=False):
    ps = '{} [{}]'.format(text, '/'.join(list(options)))

    if option_range:
        ps += '/[{}..{}]'.format(option_range.start, option_range.stop - 1)

    ps += ' '

    try:
        while True:
            user_input = input(ps)

            if user_input:
                # int
                if option_range:
                    try:
                        int_user_input = int(user_input)

                        if int_user_input in option_range:
                            return int_user_input

                    except ValueError:
                        pass

                # str
                user_input = user_input[0]

            if user_input and user_input in options:
                return user_input

            if not user_input and default:
                return default

            if not no_color:
                ps = red(ps)

    except (KeyboardInterrupt, EOFError):
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


def shell_filter(qs):
    editor = os.environ.get('EDITOR', 'vim')
    pks = []

    with tempfile.NamedTemporaryFile(mode='w+', suffix='.tmp') as tf:
        tf.write(render_to_string('croesus_core/shell/filter.txt', {'qs': qs}))
        tf.flush()
        call([editor, tf.name])
        tf.seek(0)

        for line in tf.readlines():
            if line and not line.startswith('#') and ':' in line:
                pks.append(line.split(':')[0])

    return qs.filter(pk__in=pks)


def choose_interactive(_model_names):
    class Context:
        def __init__(self, models):
            self._choosen = None
            self.kill = False
            self._classes = []
            self._names = []

            for model in models:
                model_class = apps.get_model(*model)
                model_name = model[1]

                self._names.append(model_name)
                self._classes.append(model_class)

                setattr(self, model_name, model_class)

        def choose(self, model):
            self._choosen = model

    c = Context(_model_names)
    _header = 'Choose from [{}] with c.choose()'.format(', '.join(c._names))

    while True:
        embed(header=_header)

        if type(c._choosen) in c._classes:
            return c._choosen

        if c.kill:
            return False
