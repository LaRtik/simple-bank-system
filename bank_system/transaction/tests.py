from django.test import RequestFactory, TestCase
from django.urls import reverse

from django.contrib import messages
from accounts.models import User
from bank_account.models import BankAccount, CreditCard, Currency
from bank_account.forms import MakeBankAccountForm, MakeCreditCardForm
from transaction.models import BankAccountTransaction
from transaction.forms import BankAccountTransactionForm

# Create your tests here.

class TestBankAccount(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='user', telegram_id='123', confirmed=True, first_name='Test', last_name='Tester')
        self.byn_currency = Currency.objects.create(name='BYN', description='-')
        self.usd_currency = Currency.objects.create(name='USD', description='-')
        self.byn_bank_account = BankAccount.objects.create(
            user=self.user,
            name='Test First BYN Bank Account',
            balance=2000,
            currency=self.byn_currency,
        )
        self.second_byn_bank_account = BankAccount.objects.create(
            user=self.user,
            name='Test Second BYN Bank Account',
            balance=4000,
            currency=self.byn_currency,
        )
        self.usd_bank_account = BankAccount.objects.create(
            user=self.user,
            name='Test Third USD Bank Account',
            balance=500,
            currency=self.usd_currency,
        )
        self.client.force_login(self.user)
    
    def test_form_byn_to_byn(self):
        form_data = {
            'bank_account_from': self.byn_bank_account,
            'bank_account_to': self.second_byn_bank_account.id,
            'value': 1500,
        }
        form = BankAccountTransactionForm(data=form_data, user=self.user)
        assert form.is_valid()

        resp = self.client.post('/cabinet/create_account_transaction/', form_data, follow=True)
        assert resp.status_code == 200