# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('croesus_core', '0002_Account__delete_protection'),
    ]

    operations = [
        migrations.CreateModel(
            name='Statement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('format', models.CharField(max_length=16)),
                ('data', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('comment', models.TextField(null=True, blank=True)),
                ('file_name', models.CharField(max_length=128, blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('amount', models.FloatField(null=True, blank=True)),
                ('currency', models.CharField(null=True, blank=True, max_length=8)),
                ('date', models.DateField(null=True, blank=True)),
                ('bank_code', models.CharField(null=True, blank=True, max_length=16)),
                ('account_number', models.CharField(null=True, blank=True, max_length=16)),
                ('details', models.TextField(null=True, blank=True)),
                ('final_opening_balance', models.FloatField(null=True, blank=True)),
                ('final_opening_balance_date', models.DateField(null=True, blank=True)),
                ('final_closing_balance', models.FloatField(null=True, blank=True)),
                ('final_closing_balance_date', models.DateField(null=True, blank=True)),
                ('name', models.CharField(null=True, blank=True, max_length=128)),
                ('purpose', models.TextField(null=True, blank=True)),
                ('iban', models.CharField(null=True, verbose_name='IBAN', blank=True, max_length=30)),
                ('bic', models.CharField(null=True, verbose_name='BIC', blank=True, max_length=11)),
                ('comment', models.TextField(null=True, blank=True)),
                ('person', models.ForeignKey(null=True, verbose_name='Person', to='croesus_core.Person', blank=True)),
                ('statement', models.ForeignKey(null=True, verbose_name='Statement', to='croesus_core.Statement', blank=True)),
            ],
        ),
        migrations.DeleteModel(
            name='HibiscusAccount',
        ),
        migrations.AlterUniqueTogether(
            name='hibiscusturnover',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='hibiscusturnover',
            name='person',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='turnover',
        ),
        migrations.DeleteModel(
            name='HibiscusTurnover',
        ),
        migrations.AddField(
            model_name='booking',
            name='transaction',
            field=models.ForeignKey(null=True, related_name='bookings', to='croesus_core.Transaction', blank=True, on_delete=django.db.models.deletion.PROTECT),
        ),
    ]
