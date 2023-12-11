# Generated by Django 4.2.7 on 2023-12-10 23:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bank_account', '0002_currency_bankaccount_currency_currencyrelation'),
        ('transaction', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Transaction',
            new_name='CardTransaction',
        ),
        migrations.CreateModel(
            name='BankAccountTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dt', models.DateTimeField()),
                ('value', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('bank_account_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bank_account_from', to='bank_account.bankaccount')),
                ('bank_account_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bank_account_to', to='bank_account.bankaccount')),
                ('transaction_status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transaction.transactionstatus')),
            ],
            options={
                'ordering': ['-dt'],
            },
        ),
    ]