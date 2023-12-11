from django.test import RequestFactory, TestCase
from django.urls import reverse

from django.contrib import messages
from credit.forms import CreateCreditForm
from credit.models import Credit
from accounts.models import User
from bank_account.models import BankAccount, CreditCard, Currency
from bank_account.forms import MakeBankAccountForm, MakeCreditCardForm
from transaction.models import BankAccountTransaction
from transaction.forms import BankAccountTransactionForm

# Create your tests here.


class TestCredit(TestCase):
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
        self.usd_bank_account = BankAccount.objects.create(
            user=self.user,
            name='Test Third USD Bank Account',
            balance=500,
            currency=self.usd_currency,
        )
        self.client.force_login(self.user)
        self.byn_credit = Credit.objects.create(
            name='Test credit',
            description='Test credit description',
            period_in_month=12,
            min_amount=500,
            max_amount=1000,
            percent=12,
            currency=self.byn_currency,
        )
    
    def test_byn_credit(self):
        form_data = {
            'amount': 500,
            'credit': self.byn_credit.id,
        }
        form = CreateCreditForm(data=form_data, user=self.user)
        assert not form.is_valid()

