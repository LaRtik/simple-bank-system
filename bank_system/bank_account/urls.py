from django.urls import path
from transaction.views import MoneyTransferView
from bank_account.views import (
    MakeBankAccount,
    MakeCreditCard,
    MyBankAccountView,
    MyCreditCardView,
    MyTransactionView,
)
from credit.views import CreateCreditView, MyCreditView

urlpatterns = [
	path('', MyBankAccountView.as_view(), name='bank_accounts'),
    path('bank_accounts/', MyBankAccountView.as_view(), name='bank_accounts'),
    path('create_bank_account/', MakeBankAccount.as_view(), name='create_bank_account'),
    path('credits_cards/', MyCreditCardView.as_view(), name='credit_cards'),
    path('create_credit_card/', MakeCreditCard.as_view(), name='create_credit_card'),
    path('transactions/', MyTransactionView.as_view(), name='transactions'),
    path('create_transaction/', MoneyTransferView.as_view(), name='create_transaction'),
    path('credits/', MyCreditView.as_view(), name='credits'),
    path('open_credit/', CreateCreditView.as_view(), name='open_credit'),
]
