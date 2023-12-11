import datetime
import random

from django.shortcuts import render
from bank_account.forms import MakeBankAccountForm, MakeCreditCardForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, View
from bank_account.models import BankAccount, CreditCard

from transaction.models import CardTransaction, BankAccountTransaction
from bank_account.models import BankAccount, CreditCard
from accounts.utils import LoginConfirmedRequiredMixin


class MyBankAccountView(View):
    def get(self, request, *args, **kwargs):
        bank_accounts = BankAccount.objects.filter(user=request.user)
        context = {
            'bank_accounts': bank_accounts,
        }
        return render(request, 'bank_accounts.html', context)


class MyCreditCardView(View):
    def get(self, request, *args, **kwargs):
        credit_cards = CreditCard.objects.filter(bank_account__user=request.user)
        for card in credit_cards:
            card.number = str(card.number)
            card.number = card.number[0:4] + ' ' + card.number[4:8] + ' ' + card.number[8:12] + ' ' + card.number[12:16]

        context = {
            'credit_cards': credit_cards
        }
        return render(request, 'credit_cards.html', context)


class MyTransactionView(View):
    def get(self, request, *args, **kwargs):
        transactions_card = CardTransaction.objects.filter(credit_card_from__bank_account__user=request.user)
        transactions_account = BankAccountTransaction.objects.filter(bank_account_from__user=request.user)
        context = {
            'transactions_card': transactions_card,
            'transactions_account': transactions_account
        }
        return render(request, 'transactions.html', context)


class MakeBankAccount(LoginConfirmedRequiredMixin, CreateView):
    model = BankAccount
    form_class = MakeBankAccountForm
    success_url = reverse_lazy('bank_accounts')
    template_name = 'create_bank_account.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        # form.instance.name = int(str(random.randint(1000, 9999)) + str(self.request.user.id))
        return super().form_valid(form)


class MakeCreditCard(LoginConfirmedRequiredMixin, CreateView):
    model = CreditCard
    form_class = MakeCreditCardForm
    success_url = reverse_lazy('credit_cards')
    template_name = 'create_credit_card.html'

    def form_valid(self, form):
        form.instance.cvv = random.randint(100, 999)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs



class AboutUsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'users/about_us.html')
