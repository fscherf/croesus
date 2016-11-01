from django import forms
from django.apps import apps


PERSON_TYPE_CHOICES = [
    ('m', 'Member'),
    ('l', 'Legal Person'),
]

MEMBERSHIPFEEAGREEMENT_CURRENCY_CHOICES = [
    ('EUR', 'EUR'),
]


class PersonForm(forms.ModelForm):
    type = forms.ChoiceField(
        choices=PERSON_TYPE_CHOICES,
        initial=PERSON_TYPE_CHOICES[0][0],
    )


class MembershipFeeAgreementForm(forms.ModelForm):
    repayment_period_in_months = forms.FloatField(
        label='Repayment Period In Months',
        initial=1,
    )

    currency = forms.ChoiceField(
        label='Currency',
        choices=MEMBERSHIPFEEAGREEMENT_CURRENCY_CHOICES,
        initial=MEMBERSHIPFEEAGREEMENT_CURRENCY_CHOICES[0][0],
    )

    fee = forms.FloatField(
        label='Fee',
        initial=20,
    )

    def __init__(self, *args, **kwargs):
        Person = apps.get_model('croesus_core.Person')

        super(MembershipFeeAgreementForm, self).__init__(*args, **kwargs)
        self.fields['person'].queryset = Person.objects.filter(member=True)


class MembershipFeeDebtForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        Person = apps.get_model('croesus_core.Person')

        super(MembershipFeeDebtForm, self).__init__(*args, **kwargs)
        self.fields['person'].queryset = Person.objects.filter(member=True)
