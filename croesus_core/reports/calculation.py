from django.db.models import Sum
from django.apps import apps

from datetime import date


def get_real_balance(year, month):
    Transaction = apps.get_model('croesus_core', 'Transaction')

    qs = Transaction.objects.filter(
        date__year=year,
        date__month=month,
        final_closing_balance__isnull=False
    ).distinct()

    transaction = qs.order_by('pk').last()

    return transaction.final_closing_balance, transaction


def get_balance(year, month):
    Account = apps.get_model('croesus_core', 'Account')
    Booking = apps.get_model('croesus_core', 'Booking')

    real_balance, transaction = get_real_balance(year, month)

    period = date(year, month, 1)

    future_membership_fees = Booking.objects.filter(
        date__gt=period,
        transaction__date__lt=period,
        account=Account.objects.get_membership_fee_account(),
    ).distinct()

    balance = real_balance or 0.0 - future_membership_fees.aggregate(
        Sum('amount'),
    )['amount__sum'] or 0.0

    return balance, transaction, future_membership_fees


def get_donations(year, month):
    Account = apps.get_model('croesus_core', 'Account')
    Booking = apps.get_model('croesus_core', 'Booking')

    donations = Booking.objects.filter(
        account=Account.objects.get_donation_account(),
        date__year=year,
        date__month=month,
    ).distinct()

    donations_sum = donations.aggregate(Sum('amount'))['amount__sum']

    return donations_sum, donations


def get_membership_fees(year, month):
    Account = apps.get_model('croesus_core', 'Account')
    Booking = apps.get_model('croesus_core', 'Booking')

    membership_fees = Booking.objects.filter(
        account=Account.objects.get_membership_fee_account(),
        date__year=year,
        date__month=month,
    ).distinct()

    membership_fees_sum = membership_fees.aggregate(
        Sum('amount'))['amount__sum']

    return membership_fees_sum, membership_fees


def get_expenditures(year, month):
    Transaction = apps.get_model('croesus_core', 'Transaction')

    expenditures = Transaction.objects.filter(
        date__year=year,
        date__month=month,
        amount__lt=0
    ).distinct()

    expenditures_sum = expenditures.aggregate(
        Sum('amount'),
    )['amount__sum'] * -1

    return expenditures_sum, expenditures


def get_active_members(year, month):
    Person = apps.get_model('croesus_core', 'Person')

    active_members = Person.objects.filter(
        member=True,
    ).active(
        date(year, month, 1),
    ).distinct()

    return active_members


def get_debts(year, month):
    MembershipFeeDebt = apps.get_model('croesus_core', 'MemberShipFeeDebt')
    Person = apps.get_model('croesus_core', 'Person')

    debts = MembershipFeeDebt.objects.filter(
        period__year=year,
        period__month=month,
    ).distinct()

    fees = debts.aggregate(
        expected=Sum('fee'),
        paid=Sum('bookings_amount'),
    )

    expected = fees['expected'] or 0.0
    paid = fees['paid'] or 0.0

    paying_members = Person.objects.filter(
        membershipfeedebt__in=debts.filter(paid=True),
    ).distinct()

    members_behind = Person.objects.filter(
        membershipfeedebt__in=debts.filter(paid=False),
    ).distinct()

    return expected, paid, paying_members, members_behind, debts
