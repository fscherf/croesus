from django.test import TestCase


class BookingTestCase(TestCase):
    def test_basic_bookings(self):
        from croesus_core.models import HibiscusTurnover, Account, Booking

        # create accounts
        donations_account = Account.objects.create(
            name='Donations')

        membership_fees_account = Account.objects.create(
            name='Membership Fees')

        # create turnover
        turnover = HibiscusTurnover.objects.create(
            account_id=1,
            turnover_id=1,
            amount=25.0,
        )

        # book membership fees and donations
        membership_fee_booking = turnover.book(membership_fees_account, 20.0)
        donation_booking = turnover.book(donations_account, 5.0)

        # run checks
        self.assertEqual(Booking.objects.all().count(), 2)

        self.assertEqual(
            Booking.objects.get(
                account=membership_fees_account,
                turnover=turnover,
                amount=20.0,
            ).pk,
            membership_fee_booking.pk,
        )

        self.assertEqual(
            Booking.objects.get(
                account=donations_account,
                turnover=turnover,
                amount=5.0,
            ).pk,
            donation_booking.pk,
        )

    def test_booking_amounts(self):
        from croesus_core.models import HibiscusTurnover, Account

        # create account
        account = Account.objects.create(name='Account')

        # create turnover
        turnover = HibiscusTurnover.objects.create(
            account_id=1,
            turnover_id=1,
            amount=20.0,
        )

        # test underbooked on empty bookings
        self.assertEqual(
            HibiscusTurnover.objects.count(), 1)

        self.assertEqual(
            HibiscusTurnover.objects.first().bookings_amount, None)

        self.assertEqual(
            HibiscusTurnover.objects.filter(
                underbooked=True,
            ).count(),
            1,
        )

        self.assertEqual(
            HibiscusTurnover.objects.filter(
                underbooked=False,
            ).count(),
            0,
        )

        self.assertEqual(
            HibiscusTurnover.objects.filter(
                booked=True,
            ).count(),
            0,
        )

        self.assertEqual(
            HibiscusTurnover.objects.filter(
                booked=False,
            ).count(),
            1,
        )

        self.assertEqual(
            HibiscusTurnover.objects.filter(
                overbooked=True,
            ).count(),
            0,
        )

        self.assertEqual(
            HibiscusTurnover.objects.filter(
                overbooked=False,
            ).count(),
            1,
        )

        # test underbooked
        turnover.book(account, 5.0)

        self.assertEqual(
            HibiscusTurnover.objects.count(), 1)

        self.assertEqual(
            HibiscusTurnover.objects.first().bookings_amount, 5.0)

        self.assertEqual(
            HibiscusTurnover.objects.filter(
                underbooked=True,
            ).count(),
            1,
        )

        self.assertEqual(
            HibiscusTurnover.objects.filter(
                underbooked=False,
            ).count(),
            0,
        )

        self.assertEqual(
            HibiscusTurnover.objects.filter(
                booked=True,
            ).count(),
            0,
        )

        self.assertEqual(
            HibiscusTurnover.objects.filter(
                booked=False,
            ).count(),
            1,
        )

        self.assertEqual(
            HibiscusTurnover.objects.filter(
                overbooked=True,
            ).count(),
            0,
        )

        self.assertEqual(
            HibiscusTurnover.objects.filter(
                overbooked=False,
            ).count(),
            1,
        )

        # test booked
        turnover.book(account, 15.0)

        self.assertEqual(
            HibiscusTurnover.objects.count(), 1)

        self.assertEqual(
            HibiscusTurnover.objects.first().bookings_amount, 20.0)

        self.assertEqual(
            HibiscusTurnover.objects.filter(
                underbooked=True,
            ).count(),
            0,
        )

        self.assertEqual(
            HibiscusTurnover.objects.filter(
                underbooked=False,
            ).count(),
            1,
        )

        self.assertEqual(
            HibiscusTurnover.objects.filter(
                booked=True,
            ).count(),
            1,
        )

        self.assertEqual(
            HibiscusTurnover.objects.filter(
                booked=False,
            ).count(),
            0,
        )

        self.assertEqual(
            HibiscusTurnover.objects.filter(
                overbooked=True,
            ).count(),
            0,
        )

        self.assertEqual(
            HibiscusTurnover.objects.filter(
                overbooked=False,
            ).count(),
            1,
        )

        # test overbooked
        turnover.book(account, 6.50)
        turnover.book(account, 3.50)

        self.assertEqual(
            HibiscusTurnover.objects.count(), 1)

        self.assertEqual(
            HibiscusTurnover.objects.first().bookings_amount, 30.0)

        self.assertEqual(
            HibiscusTurnover.objects.filter(
                underbooked=True,
            ).count(),
            0,
        )

        self.assertEqual(
            HibiscusTurnover.objects.filter(
                underbooked=False,
            ).count(),
            1,
        )

        self.assertEqual(
            HibiscusTurnover.objects.filter(
                booked=True,
            ).count(),
            1,
        )

        self.assertEqual(
            HibiscusTurnover.objects.filter(
                booked=False,
            ).count(),
            0,
        )

        self.assertEqual(
            HibiscusTurnover.objects.filter(
                overbooked=True,
            ).count(),
            1,
        )

        self.assertEqual(
            HibiscusTurnover.objects.filter(
                overbooked=False,
            ).count(),
            0,
        )
