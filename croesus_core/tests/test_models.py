from django.test import TestCase


class ModelTestCase(TestCase):
    def test_transaction_delete(self):
        from django.db.models import ProtectedError

        from croesus_core.models import Transaction, Account

        # transaction without bookings
        t1 = Transaction.objects.create(
            amount=20.0,
        )

        t1.delete()

        # transaction with bookings
        t2 = Transaction.objects.create(
            amount=20.0,
        )

        t2.book(Account.objects.create(name='Account'), 10.0)

        with self.assertRaises(ProtectedError):
            t2.delete()

        t2.bookings.all().delete()
        t2.delete()

    def test_account_delete(self):
        from django.db.models import ProtectedError

        from croesus_core.models import Account, Booking

        # account without bookings
        a1 = Account.objects.create(name='a1')

        a1.delete()

        # account without bookings
        a2 = Account.objects.create(name='a2')
        booking = Booking.objects.create(account=a2, amount=10.0)

        with self.assertRaises(ProtectedError):
            a2.delete()

        booking.delete()
        a2.delete()

    def test_person_types(self):
        from croesus_core.models import Person

        Person.objects.create(
            name='Alice',
            type=Person.MEMBER,
        )

        Person.objects.create(
            name='Landlord',
            type=Person.LEGAL_PERSON,
        )

        # member
        self.assertEqual(Person.objects.filter(member=True).count(), 1)

        self.assertEqual(
            Person.objects.filter(member=True).first().name, 'Alice')

        self.assertEqual(
            Person.objects.filter(member=False).first().name, 'Landlord')

        # legal_person
        self.assertEqual(Person.objects.filter(legal_person=True).count(), 1)

        self.assertEqual(
            Person.objects.filter(legal_person=True).first().name, 'Landlord')

        self.assertEqual(
            Person.objects.filter(legal_person=False).first().name, 'Alice')
