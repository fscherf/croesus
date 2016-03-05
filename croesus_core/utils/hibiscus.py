from xmlrpc.client import ServerProxy
from dateutil.parser import parse
import ssl


class HibiscusProxy(object):
    def __init__(self, username, password, protocol='https', host='localhost',
                 port=8080, verify=True):
        """
        see http://www.willuhn.de/wiki/doku.php?id=develop:xmlrpc:init
        """

        if not verify:
            context = ssl._create_unverified_context()

        else:
            context = None

        self._proxy = ServerProxy('{}://{}:{}@{}:{}/xmlrpc/'.format(
            protocol, username, password, host, port), context=context)

    @property
    def accounts(self):
        konten = []

        for i in self._proxy.hibiscus.xmlrpc.konto.find():
            i['balance'] = float(i['saldo'])
            i['balance_datum'] = parse(i['saldo_datum'])
            i['balance_available'] = float(i['saldo_available'])

            i['account_id'] = int(i['id'])
            i.pop('id')

            i['bank_name'] =\
                self._proxy.hibiscus.xmlrpc.konto.getBankname(i['blz'])

            konten.append(i)

        return konten

    def turnovers(self, raw=False, reverse=True, query={}):
        """
        https://www.willuhn.de/wiki/doku.php?id=develop:xmlrpc:umsatz
        """

        if 'datum:min' not in query:
            query['datum:min'] = '01.01.1970'

        if 'datum:max' not in query:
            query['datum:max'] = '31.12.2999'

        umsaetze = self._proxy.hibiscus.xmlrpc.umsatz.list(query)

        if reverse:
            umsaetze = umsaetze[::-1]

        for umsatz in umsaetze:
            if not raw:
                umsatz = {
                    'account_id':                  int(umsatz['konto_id']),
                    'turnover_id':                 int(umsatz['id']),
                    'amount':                      float(umsatz['betrag']),
                    'balance':                     float(umsatz['saldo']),
                    'commercial_transaction_code': int(umsatz['gvcode']),
                    'primanota':                   int(umsatz['primanota']),
                    'date':                        parse(umsatz['datum']),
                    'value_date':                  parse(umsatz['valuta']),
                    'name':                        umsatz['empfaenger_name'],
                    'iban':                        umsatz['empfaenger_konto'],
                    'bic':                         umsatz['empfaenger_blz'],
                    'type':                        umsatz['art'],
                    'purpose':                     umsatz['zweck'],
                    'comment':                     umsatz['kommentar'],
                    'customer_ref':                umsatz['customer_ref'],
                }

            yield umsatz
