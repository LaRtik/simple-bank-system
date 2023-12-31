from datetime import datetime
import decimal

from bank_account.models import BankAccount
from credit.models import CreditTransaction

class CreditPaymentMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.last_time_check = None
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        response = self.get_response(request)
        
        if not self.last_time_check or (datetime.now() - self.last_time_check).total_seconds() > 24 * 60 * 60:
            self.last_time_check = datetime.now()

            # checking credits
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

            # checking deposits
            bank_accounts = BankAccount.objects.all()
            for bank_account in bank_accounts:
                bank_account.balance *= decimal.Decimal(1.0002)
                bank_account.save()
            

        # Code to be executed for each request/response after
        # the view is called.

        return response