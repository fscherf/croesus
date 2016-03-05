from django.test import TestCase


class ModelTestCase(TestCase):
    def test_hibiscus_turnover_unique(self):
        from django.db.utils import IntegrityError

        from croesus_core.models import HibiscusTurnover

        HibiscusTurnover.objects.create(
            account_id=1,
            turnover_id=1,
            amount=20.0,
        )

        HibiscusTurnover.objects.create(
            account_id=1,
            turnover_id=2,
            amount=20.0,
        )

        with self.assertRaises(IntegrityError):
            HibiscusTurnover.objects.create(
                account_id=1,
                turnover_id=2,
                amount=20.0,
            )

    def test_hibiscus_turnover_delete(self):
        from django.db.models import ProtectedError

        from croesus_core.models import HibiscusTurnover, Account

        # turnover without bookings
        t1 = HibiscusTurnover.objects.create(
            account_id=1,
            turnover_id=1,
            amount=20.0,
        )

        t1.delete()

        # turnover with bookings
        t2 = HibiscusTurnover.objects.create(
            account_id=1,
            turnover_id=2,
            amount=20.0,
        )

        t2.book(Account.objects.create(name='Account'), 10.0)

        with self.assertRaises(ProtectedError):
            t2.delete()

        t2.bookings.all().delete()
        t2.delete()

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
