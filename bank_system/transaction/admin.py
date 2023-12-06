from django.contrib import admin

from transaction.models import TransactionStatus, Transaction

admin.site.register(Transaction)
admin.site.register(TransactionStatus)
