import datetime
from credit.models import CreditTransaction

from celery import shared_task

@shared_task
def execute_credit_transactions():
    transactions = CreditTransaction.objects.filter(dt__date__lte=datetime.date().today())
    print(transactions)