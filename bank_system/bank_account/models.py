from django.db import models
from accounts.models import User


class Currency(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class CurrencyRelation(models.Model):
    class Meta:
        unique_together = (('currency_from', 'currency_to'),)

    currency_from = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='relations_from')
    currency_to = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='relations_to')
    coefficient_buy = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    coefficient_sell = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    def __str__(self):
        return f'{self.currency_from}\{self.currency_to}'


class BankAccount(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.DecimalField(
        default=0,
        max_digits=12,
        decimal_places=2
    )
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class CreditCard(models.Model):
    number = models.CharField(max_length=16, primary_key=True)
    owner_name = models.CharField(max_length=19)
    date_to = models.DateField()
    cvv = models.IntegerField()
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)

    def __str__(self):
        return self.number
