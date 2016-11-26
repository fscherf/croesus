from django.test import TransactionTestCase


class MembershipFeeDebtTestCase(TransactionTestCase):
    def test_create_debts(self):
        """
        1970             | Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dez
                         |   1   2   3   4   5   6   7   8   9  10  11  12
        -----------------+------------------------------------------------
        agreement        |   x   x   x   x   x   x   x   x   x   x   x   x
        payment required |   x                       x
        """

        from croesus_core.models import (
            MembershipFeeAgreement,
            MembershipFeeDebt,
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
            repayment_period_in_months=6,
            fee=10,
            currency='EUR',
            start=date(1970, 1, 1),
        )

        MembershipFeeDebt.objects.create_for([
            date(1970, 1, 1),
            date(1970, 2, 1),
            date(1970, 3, 1),
            date(1970, 4, 1),
            date(1970, 5, 1),
            date(1970, 6, 1),
            date(1970, 7, 1),
            date(1970, 8, 1),
            date(1970, 9, 1),
            date(1970, 10, 1),
            date(1970, 11, 1),
            date(1970, 12, 1),
        ])

        self.assertEqual(alice.membershipfeedebt_set.all().count(), 2)

        self.assertEqual(
            alice.membershipfeedebt_set.filter(
                period__in=[date(1970, 1, 1), date(1970, 7, 1)],
                fee=10,
            ).count(),
            2,
        )

    def test_debt_bookings(self):
        from croesus_core.models import (
            MembershipFeeDebt,
            Transaction,
            Account,
            Person,
        )

        from datetime import date

        alice = Person.objects.create(name='alice')

        debt = MembershipFeeDebt.objects.create(
            period=date(1970, 1, 1),
            person=alice,
            fee=20.0,
        )

        account = Account.objects.create(name='Account')

        transaction = Transaction.objects.create(
            amount=200.0,
        )

        # test unpaid on empty bookings
        self.assertEqual(
            MembershipFeeDebt.objects.count(), 1)

        self.assertEqual(
            MembershipFeeDebt.objects.first().bookings_amount, None)

        self.assertEqual(
            MembershipFeeDebt.objects.filter(
                unpaid=True,
            ).count(),
            1,
        )

        self.assertEqual(
            MembershipFeeDebt.objects.filter(
                unpaid=False,
            ).count(),
            0,
        )

        self.assertEqual(
            MembershipFeeDebt.objects.filter(
                paid=True,
            ).count(),
            0,
        )

        self.assertEqual(
            MembershipFeeDebt.objects.filter(
                paid=False,
            ).count(),
            1,
        )

        self.assertEqual(
            MembershipFeeDebt.objects.filter(
                overpaid=True,
            ).count(),
            0,
        )

        self.assertEqual(
            MembershipFeeDebt.objects.filter(
                overpaid=False,
            ).count(),
            1,
        )

        # test unpaid
        debt.bookings.add(transaction.book(account, 10.0))
        debt.save()

        self.assertEqual(
            MembershipFeeDebt.objects.count(), 1)

        self.assertEqual(
            MembershipFeeDebt.objects.first().bookings_amount, 10.0)

        self.assertEqual(
            MembershipFeeDebt.objects.filter(
                unpaid=True,
            ).count(),
            1,
        )

        self.assertEqual(
            MembershipFeeDebt.objects.filter(
                unpaid=False,
            ).count(),
            0,
        )

        self.assertEqual(
            MembershipFeeDebt.objects.filter(
                paid=True,
            ).count(),
            0,
        )

        self.assertEqual(
            MembershipFeeDebt.objects.filter(
                paid=False,
            ).count(),
            1,
        )

        self.assertEqual(
            MembershipFeeDebt.objects.filter(
                overpaid=True,
            ).count(),
            0,
        )

        self.assertEqual(
            MembershipFeeDebt.objects.filter(
                overpaid=False,
            ).count(),
            1,
        )

        # test paid
        debt.bookings.add(transaction.book(account, 10.0))
        debt.save()

        self.assertEqual(
            MembershipFeeDebt.objects.count(), 1)

        self.assertEqual(
            MembershipFeeDebt.objects.first().bookings_amount, 20.0)

        self.assertEqual(
            MembershipFeeDebt.objects.filter(
                unpaid=True,
            ).count(),
            0,
        )

        self.assertEqual(
            MembershipFeeDebt.objects.filter(
                unpaid=False,
            ).count(),
            1,
        )

        self.assertEqual(
            MembershipFeeDebt.objects.filter(
                paid=True,
            ).count(),
            1,
        )

        self.assertEqual(
            MembershipFeeDebt.objects.filter(
                paid=False,
            ).count(),
            0,
        )

        self.assertEqual(
            MembershipFeeDebt.objects.filter(
                overpaid=True,
            ).count(),
            0,
        )

        self.assertEqual(
            MembershipFeeDebt.objects.filter(
                overpaid=False,
            ).count(),
            1,
        )

        # test overpaid
        debt.bookings.add(transaction.book(account, 5.50))
        debt.bookings.add(transaction.book(account, 4.50))
        debt.save()

        self.assertEqual(
            MembershipFeeDebt.objects.count(), 1)

        self.assertEqual(
            MembershipFeeDebt.objects.first().bookings_amount, 30.0)

        self.assertEqual(
            MembershipFeeDebt.objects.filter(
                unpaid=True,
            ).count(),
            0,
        )

        self.assertEqual(
            MembershipFeeDebt.objects.filter(
                unpaid=False,
            ).count(),
            1,
        )

        self.assertEqual(
            MembershipFeeDebt.objects.filter(
                paid=True,
            ).count(),
            1,
        )

        self.assertEqual(
            MembershipFeeDebt.objects.filter(
                paid=False,
            ).count(),
            0,
        )

        self.assertEqual(
            MembershipFeeDebt.objects.filter(
                overpaid=True,
            ).count(),
            1,
        )

        self.assertEqual(
            MembershipFeeDebt.objects.filter(
                overpaid=False,
            ).count(),
            0,
        )
