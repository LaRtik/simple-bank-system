import calendar
import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from bank_account.models import BankAccount
from django.contrib import messages
from accounts.utils import LoginConfirmedRequiredMixin

from transaction.models import CardTransaction


from credit.forms import CreateCreditForm, EditCreditForm

from credit.models import Credit, CreditTransaction

from credit.models import UserCredit


def make_credit_transactions(credit):
    # константы из формулы 3/4 лабы
    i = credit.credit.percent
    n = credit.credit.period_in_month
    k = (i / 1200 * ((1 + i / 1200) ** n)) / ((1 + i / 1200) ** n - 1)
    current_date = datetime.datetime.now()
    first = current_date.replace(day=1, month=current_date.month)
    for j in range(credit.credit.period_in_month):
        # я хз как прибавлять ровно месяц по другому
        sum_mont = 0
        for h in range(first.month, first.month + j + 1):
            _, month_days = calendar.monthrange(first.year, i)
            sum_mont += month_days
        CreditTransaction.objects.create(
            dt=first + datetime.timedelta(days=sum_mont),
            amount=float(credit.amount) * k,
            credit=credit
        )


class MyCreditView(View):
    def get(self, request, *args, **kwargs):
        credits = UserCredit.objects.filter(bank_account__user=request.user)
        context = {
            'credits': credits
        }
        return render(request, 'credits.html', context)


class CreditView(View):
    def get(self, request, *args, **kwargs):
        credits = Credit.objects.all()
        context = {
            'credits': credits
        }
        return render(request, 'available_credits.html', context)


class CreateCreditView(LoginConfirmedRequiredMixin, CreateView):
    model = CardTransaction
    form_class = CreateCreditForm
    template_name = 'open_credit.html'
    success_url = reverse_lazy('credits')

    def form_valid(self, form):
        form.instance.credit = form.cleaned_data['credit']
        form.instance.bank_account = form.cleaned_data['bank_account']
        form.instance.status = "In progress"
        form.instance.amount = form.cleaned_data['amount']
        form.instance.credits = Credit.objects.all()

        if BankAccount.objects.filter(name=form.instance.bank_account).first().currency != Credit.objects.filter(name=form.instance.credit).first().currency:

            messages.success(self.request, "Request is not accepted. Currencies of credit and bank account are different!")
            return super().form_invalid(form)

        credit = form.save()

        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class EditCreditView(LoginConfirmedRequiredMixin, UpdateView):
    model = UserCredit
    form_class = EditCreditForm
    template_name = 'edit_credit.html'
    success_url = reverse_lazy('credits')

    def form_valid(self, form):
        form.instance.bank_account = form.cleaned_data['bank_account']

        if BankAccount.objects.filter(name=form.instance.bank_account).first().currency != self.object.credit.currency:
            messages.success(self.request, "Request is not accepted. Currencies of credit and bank account are different!")
            return self.form_invalid(form)

        form.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    

class DetailsCreditView(LoginConfirmedRequiredMixin, DetailView):
    def get(self, request, *args, **kwargs):
        credit_id = kwargs.get('pk')
        payments = CreditTransaction.objects.filter(credit=credit_id, credit__status='Approved')
        context = {
            'payments': payments
        }
        return render(request, 'credit_transactions.html', context)
