from copy import copy
import mt940
import re

from .iban import compact

TRANSACTION_DETAILS_RE = re.compile(r'^([0-9]+)(?P<delimiter>.)')

TRANSACTION_DETAILS_PROTOTYPE = {
    'iban': '',
    'bic': '',
    'name': '',
    'purpose': '',
}


mt940.tags.BalanceBase.scope = mt940.models.Transaction


def parse_mt940(data):
    # Taken from the official docs:
    #
    # The currency has to be set manually when setting the BalanceBase scope
    # to Transaction.
    transactions = mt940.models.Transactions(processors=dict(
        pre_statement=[
            mt940.processors.add_currency_pre_processor('EUR'),
        ],
    ))

    transactions.parse(data)

    return transactions


def parse_mt940_transaction_details(details, bank_code='default'):
    return TRANSACTION_DETAILS_PARSERS[bank_code](details)


def parse_mt940_transaction_details_sparkasse_hildesheim(details):
    data = copy(TRANSACTION_DETAILS_PROTOTYPE)

    # find delimeter
    try:
        delimiter = TRANSACTION_DETAILS_RE.match(
            details).groupdict()['delimiter']

    except:
        return data

    # \n as delimiter is not implemented
    if delimiter == '\n':
        return data

    details = details.replace('\n', '').split(delimiter)
    details = {int(i[:2]): i[2:] for i in details}

    # iban, bic, name
    if 30 in details:
        data['bic'] = details[30]

    if 31 in details:
        data['iban'] = compact(details[31])

    if 32 in details:
        data['name'] = details[32]

    # purpose
    purpose_fields = filter(lambda x: x if 19 < x[0] < 30 else None,
                            details.items())

    purpose_fields = sorted(purpose_fields, key=lambda x: x[0])

    data['purpose'] = ''.join([i[1] for i in purpose_fields])

    return data


TRANSACTION_DETAILS_PARSERS = {
    '25950130': parse_mt940_transaction_details_sparkasse_hildesheim,
    'default': parse_mt940_transaction_details_sparkasse_hildesheim,
}
