import re

COUNTRY_CODES = {
    'AD': (24, 'Andorra'),
    'AE': (23, 'United Arab Emirates'),
    'AL': (28, 'Albania'),
    'AT': (20, 'Austria'),
    'AZ': (28, 'Azerbaijan'),
    'BA': (20, 'Bosnia and Herzegovina'),
    'BE': (16, 'Belgium'),
    'BG': (22, 'Bulgaria'),
    'BH': (22, 'Bahrain'),
    'BR': (29, 'Brazil'),
    'CH': (21, 'Switzerland'),
    'CR': (21, 'Costa Rica'),
    'CY': (28, 'Cyprus'),
    'CZ': (24, 'Czech Republic'),
    'DE': (22, 'Germany'),
    'DK': (18, 'Denmark'),
    'DO': (28, 'Dominican Republic'),
    'EE': (20, 'Estonia'),
    'ES': (24, 'Spain'),
    'FI': (18, 'Finland'),
    'FO': (18, 'Faroe Islands'),
    'FR': (27, 'France'),
    'GB': (22, 'United Kingdom'),
    'GE': (22, 'Georgia'),
    'GI': (23, 'Gibraltar'),
    'GL': (18, 'Greenland'),
    'GR': (27, 'Greece'),
    'GT': (28, 'Guatemala'),
    'HR': (21, 'Croatia'),
    'HU': (28, 'Hungary'),
    'IE': (22, 'Republic of Ireland'),
    'IL': (23, 'Israel'),
    'IS': (26, 'Iceland'),
    'IT': (27, 'Italy'),
    'JO': (30, 'Jordan'),
    'KW': (30, 'Kuwait'),
    'KZ': (20, 'Kazakhstan'),
    'LB': (28, 'Lebanon'),
    'LI': (21, 'Liechtenstein'),
    'LT': (20, 'Lithuania'),
    'LU': (20, 'Luxembourg'),
    'LV': (21, 'Latvia'),
    'MC': (27, 'Monaco'),
    'MD': (24, 'Moldova'),
    'ME': (22, 'Montenegro'),
    'MK': (19, 'Republic of Macedonia'),
    'MR': (27, 'Mauritania'),
    'MT': (31, 'Malta'),
    'MU': (30, 'Mauritius'),
    'NL': (18, 'Netherlands'),
    'NO': (15, 'Norway'),
    'PK': (24, 'Pakistan'),
    'PL': (28, 'Poland'),
    'PS': (29, 'Palestinian territories'),
    'PT': (25, 'Portugal'),
    'QA': (29, 'Qatar'),
    'RO': (24, 'Romania'),
    'RS': (22, 'Serbia'),
    'SA': (24, 'Saudi Arabia'),
    'SE': (24, 'Sweden'),
    'SI': (19, 'Slovenia'),
    'SK': (24, 'Slovakia'),
    'SM': (27, 'San Marino'),
    'TL': (23, 'East Timor'),
    'TN': (24, 'Tunisia'),
    'TR': (26, 'Turkey'),
    'UA': (29, 'Ukraine'),
    'VG': (24, 'British Virgin Islands'),
    'XK': (20, 'Kosovo'),
}

IBAN_COMPACT_RE = re.compile(r'[^A-Z0-9]')

_country_codes = []
_iban_lengths = []

for k, v in COUNTRY_CODES.items():
    _country_codes.append(k)
    _iban_lengths.append(v[0])

IBAN_RE = re.compile(
    '^(({})'.format(')|('.join(_country_codes)) +
    ')([0-9]{' +
    str(min(_iban_lengths)) +
    ',' +
    str(max(_iban_lengths)) +
    '})$'
)


def compact(iban):
    iban = iban.upper()

    return IBAN_COMPACT_RE.sub('', iban)


def format(iban, separator=' '):
    iban = compact(iban)

    return separator.join(iban[i:i + 4] for i in range(0, len(iban), 4))


def is_valid(iban, convert=True):
    if convert:
        iban = compact(iban)

    country_code = iban[:2]

    if country_code not in COUNTRY_CODES:
        return False, 'IBAN country code "{}" is unknown.'.format(country_code)

    if not IBAN_RE.match(iban):
        return False, 'IBAN contains illegal characters.'

    if not len(iban) == COUNTRY_CODES[country_code][0]:
        return False, 'IBANs with country code {} have to contain {} characters.'.format(  # NOQA
            country_code, COUNTRY_CODES[country_code][0]
        )

    return True, ''


def compare(iban_a, iban_b):
    return compact(iban_a) == compact(iban_b)
