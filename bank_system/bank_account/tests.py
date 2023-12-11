from django.test import RequestFactory, TestCase
from django.urls import reverse

from accounts.models import User
from bank_account.models import BankAccount, CreditCard, Currency
from bank_account.forms import MakeBankAccountForm, MakeCreditCardForm

# Create your tests here.

class TestBankAccount(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='user', telegram_id='123', confirmed=True, first_name='Test', last_name='Tester')
        self.currency = Currency.objects.create(name='USD', description='-')
        self.first_bank_account = BankAccount.objects.create(
            user=self.user,
            name='Test First Bank Account',
            balance=1233,
            currency=self.currency,
        )
        self.second_bank_account = BankAccount.objects.create(
            user=self.user,
            name='Test Second Bank Account',
            balance=1235,
            currency=self.currency,
        )

    def test_form(self):
        form_data = {
            'bank_account': self.first_bank_account
        }
        form = MakeCreditCardForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())

        form_data = {
            'name': 'this is test',
            'currency': self.currency,
        }
        form = MakeBankAccountForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_data = {
            'amount': 228,
            'bank_account': self.first_bank_account,
        }

    def test_logic(self):
        form_data = {
            'value': 1,
            'bank_account_from': self.first_bank_account,
            'bank_account_to': self.second_bank_account
        }
        resp = self.client.post(reverse('create_account_transaction'), form_data)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(self.first_bank_account.balance, 1233)
        self.assertEqual(self.second_bank_account.balance, 1235)

        form_data = {
            'owner_name': 'date',
            'bank_account': self.first_bank_account
        }
        resp = self.client.post(reverse('create_credit_card'), form_data)
        self.assertEqual(resp.status_code, 302)
        self.assertIsNotNone(CreditCard.objects.all())

        form_data = {
            'currency': self.currency,
        }
        resp = self.client.post(reverse('create_bank_account'), form_data)
        self.assertEqual(resp.status_code, 302)
        self.assertIsNotNone(BankAccount.objects.all())