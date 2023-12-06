from django.contrib import admin

from credit.models import Credit, UserCredit, CreditTransaction

admin.site.register(Credit)
admin.site.register(UserCredit)
admin.site.register(CreditTransaction)