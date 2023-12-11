from datetime import datetime
import decimal
from credit.models import CreditTransaction

class CreditPaymentMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.last_time_check = datetime.now()
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        response = self.get_response(request)
        
        if (datetime.now() - self.last_time_check).total_seconds() > 24 * 60 * 60:
            self.last_time_check = datetime.now()
            transactions = CreditTransaction.objects.filter(dt__lt=datetime.now())
            for transaction in transactions:
                if transaction.amount > 0:
                    bank_account = transaction.credit.bank_account
                    if transaction.amount <= bank_account.balance:
                        bank_account.balance -= transaction.amount
                        bank_account.save()

                        transaction.amount = 0
                        transaction.save()
                    else:
                        transaction.amount *= decimal.Decimal(1.011)
                        transaction.save()
        # Code to be executed for each request/response after
        # the view is called.

        return response