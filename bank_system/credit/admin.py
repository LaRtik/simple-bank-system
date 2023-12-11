from django.contrib import admin

from credit.models import Credit, UserCredit, CreditTransaction


class CreditTransactionAdmin(admin.ModelAdmin):
	list_display = ["dt", "credit", "amount"]
	list_filter = ["credit"]
     
admin.site.register(Credit)
admin.site.register(UserCredit)
admin.site.register(CreditTransaction, CreditTransactionAdmin)
