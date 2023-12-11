from django.contrib import admin
from bank_account.models import (
    BankAccount,
    CreditCard,
	Currency,
	CurrencyRelation,
)

class BankAccountAdmin(admin.ModelAdmin):
	list_display = ["id", "name", "user", "balance"]
	
class CreditCardAdmin(admin.ModelAdmin):
	list_display = ["number", "owner_name", "date_to", "bank_account"]


admin.site.register(BankAccount, BankAccountAdmin)
admin.site.register(CreditCard, CreditCardAdmin)
admin.site.register(Currency)
admin.site.register(CurrencyRelation)