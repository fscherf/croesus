from django.test import TestCase


class IBANSaveTestCase(TestCase):
    def test_compact_signal_receiver(self):
        from croesus_core.models import (
            HibiscusTurnover,
            HibiscusAccount,
            PersonAccount,
            Person,
        )

        # HibiscusTurnover
        turnover = HibiscusTurnover.objects.create(
            account_id=1,
            turnover_id=1,
            iban='De19 1234 1234 1234 1234 12',
        )

        self.assertEqual(turnover.iban, 'DE19123412341234123412')

        # HibiscusAccount
        hibiscus_account = HibiscusAccount.objects.create(
            account_id=1,
            iban='De19 1234 1234 1234 1234 12',
        )

        self.assertEqual(hibiscus_account.iban, 'DE19123412341234123412')

        # PersonAccount
        person = Person.objects.create(
            name='alice',
        )

        person_account = PersonAccount.objects.create(
            person=person,
            iban='De19 1234 1234 1234 1234 12',
        )

        self.assertEqual(person_account.iban, 'DE19123412341234123412')
