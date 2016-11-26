from django.test import TestCase


class IBANSaveTestCase(TestCase):
    def test_compact_signal_receiver(self):
        from croesus_core.models import (
            Transaction,
            PersonAccount,
            Person,
        )

        # Transaction
        transaction = Transaction.objects.create(
            iban='De19 1234 1234 1234 1234 12',
        )

        self.assertEqual(transaction.iban, 'DE19123412341234123412')

        # PersonAccount
        person = Person.objects.create(
            name='alice',
        )

        person_account = PersonAccount.objects.create(
            person=person,
            iban='De19 1234 1234 1234 1234 12',
        )

        self.assertEqual(person_account.iban, 'DE19123412341234123412')
