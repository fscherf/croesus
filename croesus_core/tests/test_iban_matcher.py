from django.test import TestCase


class IBANMatcherTestCase(TestCase):
    def test_iban_matcher(self):
        from croesus_core.models import (
            Transaction,
            PersonAccount,
            Person,
        )

        # alice
        alice = Person.objects.create(name='alice')

        PersonAccount.objects.create(
            person=alice,
            iban='DE12123412341234123400',
        )

        # bob
        bob = Person.objects.create(name='bob')

        PersonAccount.objects.create(
            person=bob,
            iban='DE12123412341234123401',
        )

        PersonAccount.objects.create(
            person=bob,
            iban='DE12123412341234123402',
        )

        # alice transactions
        transactions_alice = [
            Transaction.objects.create(
                iban='DE12123412341234123400',
            ).pk,
            Transaction.objects.create(
                iban='DE12123412341234123400',
            ).pk,
        ]

        # bobs transactions
        transactions_bob = [
            Transaction.objects.create(
                iban='DE12123412341234123401',
            ).pk,
            Transaction.objects.create(
                iban='DE12123412341234123402',
            ).pk,
        ]

        # unrelated transaction
        Transaction.objects.create(
            iban='DE12123412341234123403',
        )

        # run matcher
        Transaction.objects.all().match_ibans()

        # run checks
        # alice
        self.assertEqual(
            alice.transaction_set.count(),
            2,
        )

        self.assertEqual(
            alice.transaction_set.filter(
                pk__in=transactions_alice,
            ).count(),
            2,
        )

        # bob
        self.assertEqual(
            bob.transaction_set.count(),
            2,
        )

        self.assertEqual(
            bob.transaction_set.filter(
                pk__in=transactions_bob,
            ).count(),
            2,
        )

        # unrelated
        self.assertTrue(
            Transaction.objects.filter(
                iban='DE12123412341234123403',
                person__isnull=True,
            ).exists()
        )
