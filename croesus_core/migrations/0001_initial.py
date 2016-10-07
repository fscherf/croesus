# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(verbose_name='Name', unique=True, max_length=50)),
                ('comment', models.TextField(verbose_name='Comment', blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('amount', models.FloatField(verbose_name='Amount')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('comment', models.TextField(verbose_name='Comment', blank=True, null=True)),
                ('account', models.ForeignKey(to='croesus_core.Account')),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='HibiscusAccount',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('account_id', models.PositiveIntegerField(unique=True)),
                ('name', models.CharField(blank=True, null=True, max_length=100)),
                ('marking', models.CharField(blank=True, null=True, max_length=100)),
                ('customer_number', models.CharField(blank=True, null=True, max_length=25)),
                ('currency', models.CharField(blank=True, null=True, max_length=5)),
                ('iban', models.CharField(blank=True, null=True, max_length=30)),
                ('bic', models.CharField(blank=True, null=True, max_length=11)),
                ('account_number', models.CharField(blank=True, null=True, max_length=15)),
                ('bank_code', models.CharField(blank=True, null=True, max_length=9)),
                ('balance', models.FloatField(blank=True, null=True)),
                ('balance_available', models.FloatField(blank=True, null=True)),
                ('balance_date', models.DateField(blank=True, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='HibiscusTurnover',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('account_id', models.IntegerField(verbose_name='Account Id')),
                ('turnover_id', models.IntegerField(verbose_name='Turnover Id')),
                ('type', models.TextField(verbose_name='Type', blank=True, null=True)),
                ('balance', models.FloatField(verbose_name='Balance', blank=True, null=True)),
                ('amount', models.FloatField(verbose_name='Amount', blank=True, null=True)),
                ('date', models.DateField(verbose_name='Date', blank=True, null=True)),
                ('name', models.CharField(verbose_name='Name', blank=True, null=True, max_length=100)),
                ('customer_ref', models.TextField(verbose_name='Customer Ref', blank=True, null=True)),
                ('iban', models.CharField(verbose_name='IBAN', blank=True, null=True, max_length=30)),
                ('bic', models.CharField(verbose_name='BIC', blank=True, null=True, max_length=11)),
                ('purpose', models.TextField(verbose_name='Purpose', blank=True, null=True)),
                ('comment', models.TextField(verbose_name='Comment', blank=True, null=True)),
                ('commercial_transaction_code', models.PositiveIntegerField(verbose_name='Commercial Transaction Code', blank=True, null=True)),
                ('primanota', models.PositiveIntegerField(verbose_name='Primanota', blank=True, null=True)),
                ('value_date', models.DateField(blank=True, null=True)),
            ],
            options={
                'ordering': ['account_id', 'turnover_id'],
            },
        ),
        migrations.CreateModel(
            name='MembershipFeeAgreement',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('fee', models.FloatField(verbose_name='Fee')),
                ('repayment_period_in_months', models.IntegerField(verbose_name='Repayment Period In Months')),
                ('currency', models.CharField(verbose_name='Currency', max_length=5)),
                ('start', models.DateField(verbose_name='Start')),
                ('end', models.DateField(verbose_name='End', blank=True, null=True)),
                ('comment', models.TextField(verbose_name='Comment', blank=True, null=True)),
            ],
            options={
                'ordering': ['start'],
            },
        ),
        migrations.CreateModel(
            name='MembershipFeeDebt',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('period', models.DateField()),
                ('fee', models.FloatField()),
                ('comment', models.TextField(verbose_name='Comment', blank=True, null=True)),
                ('agreement', models.ForeignKey(null=True, blank=True, to='croesus_core.MembershipFeeAgreement')),
                ('bookings', models.ManyToManyField(to='croesus_core.Booking')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('type', models.CharField(verbose_name='Type', max_length=1)),
                ('name', models.CharField(verbose_name='Name', max_length=50)),
                ('surname', models.CharField(verbose_name='Surname', blank=True, null=True, max_length=50)),
                ('nickname', models.CharField(verbose_name='Nickname', blank=True, null=True, max_length=50)),
                ('email_address', models.EmailField(verbose_name='Email address', unique=True, blank=True, null=True, max_length=254)),
                ('accession', models.DateField(verbose_name='Accession', blank=True, null=True)),
                ('comment', models.TextField(verbose_name='Comment', blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PersonAccount',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(blank=True, null=True, max_length=100)),
                ('iban', models.CharField(unique=True, max_length=30)),
                ('bic', models.CharField(max_length=11)),
                ('comment', models.TextField(blank=True, null=True)),
                ('person', models.ForeignKey(to='croesus_core.Person')),
            ],
        ),
        migrations.CreateModel(
            name='PersonInactiveRule',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('start', models.DateField(verbose_name='Start')),
                ('end', models.DateField(verbose_name='End', blank=True, null=True)),
                ('comment', models.TextField(verbose_name='Comment', blank=True, null=True)),
                ('person', models.ForeignKey(to='croesus_core.Person')),
            ],
            options={
                'ordering': ['start'],
            },
        ),
        migrations.AddField(
            model_name='membershipfeedebt',
            name='person',
            field=models.ForeignKey(to='croesus_core.Person'),
        ),
        migrations.AddField(
            model_name='membershipfeeagreement',
            name='person',
            field=models.ForeignKey(to='croesus_core.Person'),
        ),
        migrations.AddField(
            model_name='hibiscusturnover',
            name='person',
            field=models.ForeignKey(verbose_name='Person', null=True, blank=True, to='croesus_core.Person'),
        ),
        migrations.AddField(
            model_name='booking',
            name='turnover',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, null=True, related_name='bookings', blank=True, to='croesus_core.HibiscusTurnover'),
        ),
        migrations.AlterUniqueTogether(
            name='membershipfeedebt',
            unique_together=set([('person', 'period')]),
        ),
        migrations.AlterUniqueTogether(
            name='hibiscusturnover',
            unique_together=set([('account_id', 'turnover_id')]),
        ),
    ]
