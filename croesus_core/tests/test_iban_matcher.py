from django.test import TestCase


class IBANMatcherTestCase(TestCase):
    def test_iban_matcher(self):
        from croesus_core.models import (
            HibiscusTurnover,
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

        # alice turnovers
        HibiscusTurnover.objects.create(
            account_id=1,
            turnover_id=1,
            iban='DE12123412341234123400',
        )

        HibiscusTurnover.objects.create(
            account_id=1,
            turnover_id=2,
            iban='DE12123412341234123400',
        )

        # bobs turnovers
        HibiscusTurnover.objects.create(
            account_id=1,
            turnover_id=3,
            iban='DE12123412341234123401',
        )

        HibiscusTurnover.objects.create(
            account_id=1,
            turnover_id=4,
            iban='DE12123412341234123402',
        )

        # unrelated turnover
        HibiscusTurnover.objects.create(
            account_id=1,
            turnover_id=5,
            iban='DE12123412341234123403',
        )

        # run matcher
        HibiscusTurnover.objects.all().match_ibans()

        # run checks
        # alice
        self.assertEqual(
            alice.hibiscusturnover_set.count(),
            2,
        )

        self.assertEqual(
            alice.hibiscusturnover_set.filter(
                turnover_id__in=[1, 2],
            ).count(),
            2,
        )

        # bob
        self.assertEqual(
            bob.hibiscusturnover_set.count(),
            2,
        )

        self.assertEqual(
            bob.hibiscusturnover_set.filter(
                turnover_id__in=[3, 4],
            ).count(),
            2,
        )

        # unrelated
        self.assertTrue(
            HibiscusTurnover.objects.filter(
                account_id=1,
                turnover_id=5,
                person__isnull=True,
            ).exists()
        )
