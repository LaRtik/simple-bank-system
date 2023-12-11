from django import forms
from bank_account.models import BankAccount


from credit.models import Credit, CreditTransaction, UserCredit


class CreateCreditForm(forms.ModelForm):
    class Meta:
        model = UserCredit
        fields = ['credit', 'bank_account', 'amount']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bank_account'].queryset = BankAccount.objects.filter(user=user)

    def clean(self):
        cleaned_data = super().clean()
        amount = self.cleaned_data.get('amount')
        credit = self.cleaned_data.get('credit')
        if amount is None:
            raise forms.ValidationError("Value must be lower than credit maximum value")
        else:
            if amount > credit.max_amount:
                raise forms.ValidationError("Value must be lower than credit maximum value")
            if amount < credit.min_amount:
                raise forms.ValidationError("Value must be higher than credit minimum value")
        return cleaned_data
    

class EditCreditForm(forms.ModelForm):
    class Meta:
        model = UserCredit
        fields = ['bank_account']
    
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bank_account'].queryset = BankAccount.objects.filter(user=user)

