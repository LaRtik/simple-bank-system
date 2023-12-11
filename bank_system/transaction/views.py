import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic.edit import CreateView, View, UpdateView

from bank_account.models import BankAccount, CreditCard, CurrencyRelation
from accounts.utils import LoginConfirmedRequiredMixin
from transaction.models import BankAccountTransaction, CardTransaction, TransactionStatus

from transaction.forms import BankAccountTransactionForm, CardTransactionForm


class MoneyTransferView(LoginConfirmedRequiredMixin, CreateView):
    model = CardTransaction
    form_class = CardTransactionForm
    template_name = 'transaction/money_transfer.html'
    success_url = reverse_lazy('transactions')

    def form_valid(self, form):
        credit_card_from = form.cleaned_data['credit_card_from']
        credit_card_to = CreditCard.objects.filter(number=form.cleaned_data['credit_card_to']).first()


        if credit_card_from.bank_account.balance < form.cleaned_data['value']:
            transaction_status = TransactionStatus.objects.get(type='insufficient_funds')
        else:
            transaction_status = TransactionStatus.objects.get(type='approved')

            # Update the balances of the credit cards
            credit_card_from.bank_account.balance -= form.cleaned_data['value']

            credit_card_from.bank_account.save()

            # без этого при переводе самому себе - изи деньги
            credit_card_to = CreditCard.objects.filter(number=form.cleaned_data['credit_card_to']).first()
            credit_card_to.bank_account.balance += form.cleaned_data['value']
            credit_card_to.bank_account.save()

        form.instance.dt = datetime.datetime.now()
        form.instance.value = form.cleaned_data['value']
        form.instance.credit_card_from = form.cleaned_data['credit_card_from']
        form.instance.credit_card_to = credit_card_to
        form.instance.transaction_status = transaction_status

        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class BankAccountTransactionView(LoginConfirmedRequiredMixin, CreateView):
    model = BankAccountTransaction
    form_class = BankAccountTransactionForm
    template_name = 'transaction/money_transfer.html'

    success_url = reverse_lazy('transactions')

    def form_valid(self, form):
        bank_account_from = form.cleaned_data['bank_account_from']
        bank_account_to = BankAccount.objects.filter(id=form.cleaned_data['bank_account_to']).first()

        if bank_account_from == bank_account_to:
            form.instance.dt = datetime.datetime.now()
            form.instance.value = form.cleaned_data['value']
            form.instance.bank_account_from = bank_account_from
            form.instance.bank_account_to = bank_account_to
            form.instance.transaction_status = TransactionStatus.objects.get(
                type='self_transaction')
            messages.error(self.request, "You can not send money to yourself")
            return super().form_valid(form)
        coef = 1
        if bank_account_from.currency == bank_account_to.currency:
            # если одинаковые валюты
            coef = 1
        else:
            # пытаюсь найти обмен
            currency_relation_direct = CurrencyRelation.objects.filter(
                currency_from=bank_account_from.currency,
                currency_to=bank_account_to.currency
            ).first()

            currency_relation_invert = CurrencyRelation.objects.filter(
                currency_from=bank_account_to.currency,
                currency_to=bank_account_from.currency
            ).first()
            currency_relation = currency_relation_direct or currency_relation_invert

            if currency_relation is None:
                # если такого обмена нет
                transaction_status = TransactionStatus.objects.get(type='currency_pair_not_found')

                form.instance.dt = datetime.datetime.now()
                form.instance.value = form.cleaned_data['value']
                form.instance.bank_account_from = bank_account_from
                form.instance.bank_account_to = bank_account_to
                form.instance.transaction_status = transaction_status
                messages.error(self.request, "Currency pair of these bank accounts does not exists!")
                return super().form_valid(form)
            else:
                if currency_relation == currency_relation_direct:
                    coef = currency_relation.coefficient_sell
                else:
                    coef = currency_relation.coefficient_buy

        if bank_account_from.balance / coef < form.cleaned_data['value']:
            transaction_status = TransactionStatus.objects.get(type='insufficient_funds')
            messages_text = 'Insufficient Funds'
        else:
            transaction_status = TransactionStatus.objects.get(type='success')
            messages_text = 'Transation executed successfully!'

            bank_account_from.balance -= form.cleaned_data['value'] * coef

            bank_account_from.save()

            bank_account_to = BankAccount.objects.filter(id=form.cleaned_data['bank_account_to']).first()
            bank_account_to.balance += form.cleaned_data['value']
            bank_account_to.save()

        form.instance.dt = datetime.datetime.now()
        form.instance.value = form.cleaned_data['value']
        form.instance.bank_account_from = form.cleaned_data['bank_account_from']
        form.instance.bank_account_to = bank_account_to
        form.instance.transaction_status = transaction_status
        messages.success(self.request, messages_text)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs