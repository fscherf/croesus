from django.test import TestCase


class MembershipFeeAgreementTestCase(TestCase):
    def test_standart_agreement(self):
        """
        1970             | Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dez
                         |   1   2   3   4   5   6   7   8   9  10  11  12
        -----------------+------------------------------------------------
        agreement        |   x   x   x   x   x   x   x   x   x   x   x   x
        payment required |   x   x   x   x   x   x   x   x   x   x   x   x
        """

        from croesus_core.models import Person, MembershipFeeAgreement

        from datetime import date

        alice = Person.objects.create(
            name='alice',
            accession=date(1970, 1, 1),
            type='m',
        )

        MembershipFeeAgreement.objects.create(
            person=alice,
            repayment_period_in_months=1,
            fee=10,
            currency='EUR',
            start=date(1970, 1, 1),
        )

        self.assertTrue(alice.get_membership_fee_agreement(date(1970, 1, 1)))
        self.assertTrue(alice.get_membership_fee_agreement(date(1970, 2, 1)))
        self.assertTrue(alice.get_membership_fee_agreement(date(1970, 3, 1)))
        self.assertTrue(alice.get_membership_fee_agreement(date(1970, 4, 1)))
        self.assertTrue(alice.get_membership_fee_agreement(date(1970, 5, 1)))
        self.assertTrue(alice.get_membership_fee_agreement(date(1970, 6, 1)))
        self.assertTrue(alice.get_membership_fee_agreement(date(1970, 7, 1)))
        self.assertTrue(alice.get_membership_fee_agreement(date(1970, 8, 1)))
        self.assertTrue(alice.get_membership_fee_agreement(date(1970, 9, 1)))
        self.assertTrue(alice.get_membership_fee_agreement(date(1970, 10, 1)))
        self.assertTrue(alice.get_membership_fee_agreement(date(1970, 11, 1)))
        self.assertTrue(alice.get_membership_fee_agreement(date(1970, 12, 1)))
        self.assertTrue(alice.get_membership_fee_agreement(date(1971, 1, 1)))

    def test_custom_repayment_period_agreement(self):
        """
        alice
        1970             | Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dez
                         |   1   2   3   4   5   6   7   8   9  10  11  12
        -----------------+------------------------------------------------
        agreement        |   x   x   x   x   x   x   x   x   x   x   x   x
        payment required |   x           x           x           x


        bob
        1970             | Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dez
                         |   1   2   3   4   5   6   7   8   9  10  11  12
        -----------------+------------------------------------------------
        agreement        |   x   x   x   x   x   x   x   x   x   x   x   x
        payment required |   x
        """

        from croesus_core.models import Person, MembershipFeeAgreement

        from datetime import date

        # alice
        alice = Person.objects.create(
            name='alice',
            accession=date(1970, 1, 1),
            type='m',
        )

        MembershipFeeAgreement.objects.create(
            person=alice,
            repayment_period_in_months=3,
            fee=10,
            currency='EUR',
            start=date(1970, 1, 1),
        )

        # bob
        bob = Person.objects.create(
            name='bob',
            accession=date(1970, 1, 1),
            type='m',
        )

        MembershipFeeAgreement.objects.create(
            person=bob,
            repayment_period_in_months=12,
            fee=10,
            currency='EUR',
            start=date(1970, 1, 1),
        )

        # alice
        self.assertTrue(alice.get_membership_fee_agreement(date(1970, 1, 1)))
        self.assertFalse(alice.get_membership_fee_agreement(date(1970, 2, 1)))
        self.assertFalse(alice.get_membership_fee_agreement(date(1970, 3, 1)))

        self.assertTrue(alice.get_membership_fee_agreement(date(1970, 4, 1)))
        self.assertFalse(alice.get_membership_fee_agreement(date(1970, 5, 1)))
        self.assertFalse(alice.get_membership_fee_agreement(date(1970, 6, 1)))

        self.assertTrue(alice.get_membership_fee_agreement(date(1970, 7, 1)))
        self.assertFalse(alice.get_membership_fee_agreement(date(1970, 8, 1)))
        self.assertFalse(alice.get_membership_fee_agreement(date(1970, 9, 1)))

        self.assertTrue(alice.get_membership_fee_agreement(date(1970, 10, 1)))
        self.assertFalse(alice.get_membership_fee_agreement(date(1970, 11, 1)))
        self.assertFalse(alice.get_membership_fee_agreement(date(1970, 12, 1)))

        self.assertTrue(alice.get_membership_fee_agreement(date(1971, 10, 1)))
        self.assertFalse(alice.get_membership_fee_agreement(date(1971, 11, 1)))
        self.assertFalse(alice.get_membership_fee_agreement(date(1971, 12, 1)))

        # bob
        self.assertTrue(bob.get_membership_fee_agreement(date(1970, 1, 1)))
        self.assertFalse(bob.get_membership_fee_agreement(date(1970, 2, 1)))
        self.assertFalse(bob.get_membership_fee_agreement(date(1970, 3, 1)))
        self.assertFalse(bob.get_membership_fee_agreement(date(1970, 4, 1)))
        self.assertFalse(bob.get_membership_fee_agreement(date(1970, 5, 1)))
        self.assertFalse(bob.get_membership_fee_agreement(date(1970, 6, 1)))
        self.assertFalse(bob.get_membership_fee_agreement(date(1970, 7, 1)))
        self.assertFalse(bob.get_membership_fee_agreement(date(1970, 8, 1)))
        self.assertFalse(bob.get_membership_fee_agreement(date(1970, 9, 1)))
        self.assertFalse(bob.get_membership_fee_agreement(date(1970, 10, 1)))
        self.assertFalse(bob.get_membership_fee_agreement(date(1970, 11, 1)))
        self.assertFalse(bob.get_membership_fee_agreement(date(1970, 12, 1)))

        self.assertTrue(bob.get_membership_fee_agreement(date(1971, 1, 1)))

    def test_non_member_agreement(self):
        from croesus_core.models import Person, MembershipFeeAgreement

        from datetime import date

        alice = Person.objects.create(
            name='alice',
            accession=date(1970, 1, 1),
            type='l',
        )

        MembershipFeeAgreement.objects.create(
            person=alice,
            repayment_period_in_months=1,
            fee=10,
            currency='EUR',
            start=date(1970, 1, 1),
        )

        self.assertFalse(alice.get_membership_fee_agreement(date(1970, 1, 1)))

    def test_expiring_agreement(self):
        """
        1970             | Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dez
                         |   1   2   3   4   5   6   7   8   9  10  11  12
        -----------------+------------------------------------------------
        agreement        |   x   x   x   x   x   x   x   x   x   x   x   x
        payment required |   x   x   x   x   x   x
        """

        from croesus_core.models import Person, MembershipFeeAgreement

        from datetime import date

        alice = Person.objects.create(
            name='alice',
            accession=date(1970, 1, 1),
            type='m',
        )

        MembershipFeeAgreement.objects.create(
            person=alice,
            repayment_period_in_months=1,
            fee=10,
            currency='EUR',
            start=date(1970, 1, 1),
            end=date(1970, 7, 1),
        )

        self.assertTrue(alice.get_membership_fee_agreement(date(1970, 1, 1)))
        self.assertTrue(alice.get_membership_fee_agreement(date(1970, 2, 1)))
        self.assertTrue(alice.get_membership_fee_agreement(date(1970, 3, 1)))
        self.assertTrue(alice.get_membership_fee_agreement(date(1970, 4, 1)))
        self.assertTrue(alice.get_membership_fee_agreement(date(1970, 5, 1)))
        self.assertTrue(alice.get_membership_fee_agreement(date(1970, 6, 1)))
        self.assertFalse(alice.get_membership_fee_agreement(date(1970, 7, 1)))
        self.assertFalse(alice.get_membership_fee_agreement(date(1970, 8, 1)))
        self.assertFalse(alice.get_membership_fee_agreement(date(1970, 9, 1)))
        self.assertFalse(alice.get_membership_fee_agreement(date(1970, 10, 1)))
        self.assertFalse(alice.get_membership_fee_agreement(date(1970, 11, 1)))
        self.assertFalse(alice.get_membership_fee_agreement(date(1970, 12, 1)))

    def test_multiple_agreements_error(self):
        from croesus_core.models import Person, MembershipFeeAgreement

        from croesus_core.exceptions.membership_fee_agreement import (
            MultipleMembershipFeeAgreementsError,
        )

        from datetime import date

        alice = Person.objects.create(
            name='alice',
            accession=date(1970, 1, 1),
            type='m',
        )

        a1 = MembershipFeeAgreement.objects.create(
            person=alice,
            repayment_period_in_months=1,
            fee=10,
            currency='EUR',
            start=date(1970, 1, 1),
            end=date(1970, 7, 1),
        )

        a2 = MembershipFeeAgreement.objects.create(
            person=alice,
            repayment_period_in_months=1,
            fee=10,
            currency='EUR',
            start=date(1970, 6, 1),
        )

        with self.assertRaises(MultipleMembershipFeeAgreementsError) as cm:
            alice.get_membership_fee_agreement(date(1970, 6, 1))

        agreements = list(cm.exception.agreements)

        self.assertEqual(len(agreements), 2)
        self.assertIn(a1, agreements)
        self.assertIn(a2, agreements)

    def test_inactive_member(self):
        """
        1970             | Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dez
                         |   1   2   3   4   5   6   7   8   9  10  11  12
        -----------------+------------------------------------------------
        agreement        |   x   x   x   x   x   x   x   x   x   x   x   x
        inactive         |           x   x           x   x   x   x   x   x
        payment required |   x   x           x   x
        """

        from croesus_core.models import (
            MembershipFeeAgreement,
            PersonInactiveRule,
            Person,
        )

        from datetime import date

        alice = Person.objects.create(
            name='alice',
            accession=date(1970, 1, 1),
            type='m',
        )

        MembershipFeeAgreement.objects.create(
            person=alice,
            repayment_period_in_months=1,
            fee=10,
            currency='EUR',
            start=date(1970, 1, 1),
        )

        PersonInactiveRule.objects.create(
            person=alice,
            start=date(1970, 3, 1),
            end=date(1970, 5, 1),
        )

        PersonInactiveRule.objects.create(
            person=alice,
            start=date(1970, 7, 1),
        )

        self.assertTrue(alice.get_membership_fee_agreement(date(1970, 1, 1)))
        self.assertTrue(alice.get_membership_fee_agreement(date(1970, 2, 1)))

        self.assertFalse(alice.get_membership_fee_agreement(date(1970, 3, 1)))
        self.assertFalse(alice.get_membership_fee_agreement(date(1970, 4, 1)))

        self.assertTrue(alice.get_membership_fee_agreement(date(1970, 5, 1)))
        self.assertTrue(alice.get_membership_fee_agreement(date(1970, 6, 1)))

        self.assertFalse(alice.get_membership_fee_agreement(date(1970, 7, 1)))
        self.assertFalse(alice.get_membership_fee_agreement(date(1970, 8, 1)))
        self.assertFalse(alice.get_membership_fee_agreement(date(1970, 9, 1)))
        self.assertFalse(alice.get_membership_fee_agreement(date(1970, 10, 1)))
        self.assertFalse(alice.get_membership_fee_agreement(date(1970, 11, 1)))
        self.assertFalse(alice.get_membership_fee_agreement(date(1970, 12, 1)))
