# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('croesus_core', '0003_switch_from_Hibiscus_to_MT940'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='booked',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='date',
            field=models.DateField(null=True, blank=True),
        ),
    ]
