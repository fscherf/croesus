from django.test import TestCase


class BookingTestCase(TestCase):
    def test_basic_bookings(self):
        from croesus_core.models import Transaction, Account, Booking

        # create accounts
        donations_account = Account.objects.create(
            name='Donations')

        membership_fees_account = Account.objects.create(
            name='Membership Fees')

        # create transaction
        transaction = Transaction.objects.create(
            amount=25.0,
        )

        # book membership fees and donations
        membership_fee_booking = transaction.book(
            membership_fees_account, 20.0)

        donation_booking = transaction.book(donations_account, 5.0)

        # run checks
        self.assertEqual(Booking.objects.all().count(), 2)

        self.assertEqual(
            Booking.objects.get(
                account=membership_fees_account,
                transaction=transaction,
                amount=20.0,
            ).pk,
            membership_fee_booking.pk,
        )

        self.assertEqual(
            Booking.objects.get(
                account=donations_account,
                transaction=transaction,
                amount=5.0,
            ).pk,
            donation_booking.pk,
        )

    def test_booking_amounts(self):
        from croesus_core.models import Transaction, Account

        # create account
        account = Account.objects.create(name='Account')

        # create turnover
        transaction = Transaction.objects.create(
            amount=20.0,
        )

        # test underbooked on empty bookings
        self.assertEqual(
            Transaction.objects.count(), 1)

        self.assertEqual(
            Transaction.objects.first().bookings_amount, None)

        self.assertEqual(
            Transaction.objects.filter(
                underbooked=True,
            ).count(),
            1,
        )

        self.assertEqual(
            Transaction.objects.filter(
                underbooked=False,
            ).count(),
            0,
        )

        self.assertEqual(
            Transaction.objects.filter(
                booked=True,
            ).count(),
            0,
        )

        self.assertEqual(
            Transaction.objects.filter(
                booked=False,
            ).count(),
            1,
        )

        self.assertEqual(
            Transaction.objects.filter(
                overbooked=True,
            ).count(),
            0,
        )

        self.assertEqual(
            Transaction.objects.filter(
                overbooked=False,
            ).count(),
            1,
        )

        # test underbooked
        transaction.book(account, 5.0)

        self.assertEqual(
            Transaction.objects.count(), 1)

        self.assertEqual(
            Transaction.objects.first().bookings_amount, 5.0)

        self.assertEqual(
            Transaction.objects.filter(
                underbooked=True,
            ).count(),
            1,
        )

        self.assertEqual(
            Transaction.objects.filter(
                underbooked=False,
            ).count(),
            0,
        )

        self.assertEqual(
            Transaction.objects.filter(
                booked=True,
            ).count(),
            0,
        )

        self.assertEqual(
            Transaction.objects.filter(
                booked=False,
            ).count(),
            1,
        )

        self.assertEqual(
            Transaction.objects.filter(
                overbooked=True,
            ).count(),
            0,
        )

        self.assertEqual(
            Transaction.objects.filter(
                overbooked=False,
            ).count(),
            1,
        )

        # test booked
        transaction.book(account, 15.0)

        self.assertEqual(
            Transaction.objects.count(), 1)

        self.assertEqual(
            Transaction.objects.first().bookings_amount, 20.0)

        self.assertEqual(
            Transaction.objects.filter(
                underbooked=True,
            ).count(),
            0,
        )

        self.assertEqual(
            Transaction.objects.filter(
                underbooked=False,
            ).count(),
            1,
        )

        self.assertEqual(
            Transaction.objects.filter(
                booked=True,
            ).count(),
            1,
        )

        self.assertEqual(
            Transaction.objects.filter(
                booked=False,
            ).count(),
            0,
        )

        self.assertEqual(
            Transaction.objects.filter(
                overbooked=True,
            ).count(),
            0,
        )

        self.assertEqual(
            Transaction.objects.filter(
                overbooked=False,
            ).count(),
            1,
        )

        # test overbooked
        transaction.book(account, 6.50)
        transaction.book(account, 3.50)

        self.assertEqual(
            Transaction.objects.count(), 1)

        self.assertEqual(
            Transaction.objects.first().bookings_amount, 30.0)

        self.assertEqual(
            Transaction.objects.filter(
                underbooked=True,
            ).count(),
            0,
        )

        self.assertEqual(
            Transaction.objects.filter(
                underbooked=False,
            ).count(),
            1,
        )

        self.assertEqual(
            Transaction.objects.filter(
                booked=True,
            ).count(),
            1,
        )

        self.assertEqual(
            Transaction.objects.filter(
                booked=False,
            ).count(),
            0,
        )

        self.assertEqual(
            Transaction.objects.filter(
                overbooked=True,
            ).count(),
            1,
        )

        self.assertEqual(
            Transaction.objects.filter(
                overbooked=False,
            ).count(),
            0,
        )
