from django import forms
from bank_account.models import BankAccount, CreditCard

from transaction.models import BankAccountTransaction, CardTransaction


class CardTransactionForm(forms.ModelForm):
    credit_card_to = forms.CharField(max_length=16)

    class Meta:
        model = CardTransaction
        fields = ['value', 'credit_card_from']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['credit_card_from'].queryset = CreditCard.objects.filter(bank_account__user=user)

    def clean_value(self):
        value = self.cleaned_data.get('value')
        if value <= 0:
            raise forms.ValidationError("Value must be positive")
        return value

    def clean_credit_card_to(self):
        credit_card_to = self.cleaned_data.get('credit_card_to')
        credit_card_to = CreditCard.objects.filter(number=credit_card_to).first()
        if credit_card_to is None:
            raise forms.ValidationError("Incorrect credit card to")
        return credit_card_to


class BankAccountTransactionForm(forms.ModelForm):
    bank_account_to = forms.IntegerField()

    class Meta:
        model = BankAccountTransaction
        fields = ['value', 'bank_account_from']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bank_account_from'].queryset = BankAccount.objects.filter(user=user)

    def clean_value(self):
        value = self.cleaned_data.get('value')
        if value <= 0:
            raise forms.ValidationError("Value must be positive")
        return value

    def clean_bank_account_to(self):
        bank_account_to = self.cleaned_data.get('bank_account_to')
        bank_account_to = BankAccount.objects.filter(id=bank_account_to).first()
        if bank_account_to is None:
            raise forms.ValidationError("Incorrect bank account to")
        return bank_account_to.id