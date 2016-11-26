from django.test import TestCase


class IBANUtilsTestCase(TestCase):
    def test_compact(self):
        from croesus_core.utils.iban import compact

        self.assertEqual(compact('De19 1234  1234 1234-1234 12'),
                         'DE19123412341234123412',)

        self.assertEqual(compact('DE19123412341234123412'),
                         'DE19123412341234123412',)

    def test_format(self):
        from croesus_core.utils.iban import format

        self.assertEqual(format('DE19123412341234123412'),
                         'DE19 1234 1234 1234 1234 12',)

        self.assertEqual(format('DE19 1234 1234 1234 1234 12'),
                         'DE19 1234 1234 1234 1234 12',)

    def test_compare(self):
        from croesus_core.utils.iban import compare

        # equal
        self.assertTrue(compare('DE19123412341234123412',
                                'DE19 1234 1234 1234 1234 12'))

        self.assertTrue(compare('DE19 1234 1234 1234 1234 12',
                                'DE19123412341234123412'))

        self.assertTrue(compare('DE19 1234 1234 1234 1234 12',
                                'DE19 1234 1234 1234 1234 12'))

        self.assertTrue(compare('DE19123412341234123412',
                                'DE19123412341234123412'))

        # unequal
        self.assertFalse(compare('DE19123412341234123421',
                                 'DE19 1234 1234 1234 1234 12'))

        self.assertFalse(compare('DE19 1234 1234 1234 1234 21',
                                 'DE19123412341234123412'))

        self.assertFalse(compare('DE19 1234 1234 1234 1234 21',
                                 'DE19 1234 1234 1234 1234 12'))

        self.assertFalse(compare('DE19123412341234123421',
                                 'DE19123412341234123412'))

    def test_is_valid(self):
        from croesus_core.utils.iban import is_valid

        # valid IBAN
        valid, message = is_valid('DE19123412341234123412', convert=False)

        self.assertTrue(valid)
        self.assertFalse(message)

        valid, message = is_valid('De19 1234 1234 1234 1234 12')

        self.assertTrue(valid)
        self.assertFalse(message)

        valid, message = is_valid('DE19-1234-1234-1234-1234-12')

        self.assertTrue(valid)
        self.assertFalse(message)

        # invalid IBAN
        # wrong length
        valid, message = is_valid('DE1912341241234123412')

        self.assertFalse(valid)
        self.assertTrue('have to contain' in message)

        # invalid country code
        valid, message = is_valid('XX19123412341234123412')

        self.assertFalse(valid)
        self.assertTrue('is unknown' in message)

        # illegal character
        valid, message = is_valid('DEX9123412341234123412')

        self.assertFalse(valid)
        self.assertTrue('illegal character' in message)

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
