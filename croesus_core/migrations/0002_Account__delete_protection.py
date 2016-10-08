# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('croesus_core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='croesus_core.Account'),
        ),
    ]
