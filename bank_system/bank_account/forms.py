import datetime
from django import forms
from bank_account.models import BankAccount, CreditCard
from accounts.models import User
from bank_account.utils import generate_card_number


class MakeBankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ['name']


class MakeCreditCardForm(forms.ModelForm):
    class Meta:
        model = CreditCard
        fields = ['number', 'owner_name', 'date_to', 'bank_account']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user_info = User.objects.filter(username=user)[0]
        self.fields['owner_name'].initial = str.upper(user_info.first_name + ' ' + user_info.last_name)
        self.fields['owner_name'].disabled = True
        self.fields['date_to'].initial = datetime.date.today() + datetime.timedelta(days=365 * 3 + 366)
        self.fields['date_to'].disabled = True
        self.fields['number'].initial = generate_card_number()
        self.fields['number'].disabled = True
        self.fields['bank_account'].queryset = BankAccount.objects.filter(user=user)
