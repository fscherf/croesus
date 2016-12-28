from datetime import datetime

from django.template.loader import render_to_string

from ..settings import REPORT_TEMPLATES

from .calculation import (
    get_balance,
    get_real_balance,
    get_donations,
    get_active_members,
    get_debts,
    get_expenditures,
)


def render_report(year, month, template_name, date_of_report=None,
                  debug_buffer=None):

    date_of_report = date_of_report or datetime.now()
    template_path = REPORT_TEMPLATES[template_name]

    context = {
        'year': year,
        'month': month,
        'date_of_report': date_of_report,
    }

    # active members
    active_members = get_active_members(year, month)
    context['active_members'] = active_members.count()

    if debug_buffer:
        debug_buffer.write('= Active members =')
        debug_buffer.write('active_members: {}'.format(active_members.count()))
        debug_buffer.write(str(active_members))

    # balance
    balance, transaction, future_membership_fees = get_balance(year, month)
    context['balance'] = balance

    if debug_buffer:
        debug_buffer.write('\n= Balance =')
        debug_buffer.write('balance: {}'.format(balance))
        debug_buffer.write('transaction: {}'.format(repr(transaction)))
        debug_buffer.write('\nFuture membership fees')
        debug_buffer.write(str(future_membership_fees))

    # real balance
    real_balance, transaction = get_real_balance(year, month)
    context['real_balance'] = real_balance

    if debug_buffer:
        debug_buffer.write('\n= Real balance =')
        debug_buffer.write('real_balance: {}'.format(real_balance))
        debug_buffer.write('transaction: {}'.format(repr(transaction)))

    # donations
    donations_sum, donations = get_donations(year, month)
    context['donations'] = donations_sum

    if debug_buffer:
        debug_buffer.write('\n= Donations =')
        debug_buffer.write('donations_sum: {}'.format(donations_sum))
        debug_buffer.write(str(donations))

    # debts
    expected, paid, paying_members, members_behind, debts = get_debts(year,
                                                                      month)
    context['membershipfees_expected'] = expected
    context['membershipfees_paid'] = paid
    context['paying_members'] = paying_members.count()
    context['members_behind'] = members_behind.count()

    if debug_buffer:
        debug_buffer.write('\n= Debts =\n{}'.format(str(debts)))
        debug_buffer.write('\nPaying members\n{}'.format(str(paying_members)))
        debug_buffer.write('\nMembers behind\n{}'.format(str(members_behind)))

    # expenditures
    expenditures_sum, expenditures = get_expenditures(year, month)
    context['expenditures'] = expenditures_sum

    if debug_buffer:
        debug_buffer.write('\n= Expenditures =')
        debug_buffer.write('expenditures: {}'.format(expenditures_sum))
        debug_buffer.write('\n{}'.format(str(expenditures)))

    return render_to_string(template_path, context)
