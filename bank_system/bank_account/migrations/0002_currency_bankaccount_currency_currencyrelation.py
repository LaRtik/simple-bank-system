# Generated by Django 4.2.7 on 2023-12-10 21:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bank_account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('name', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='bankaccount',
            name='currency',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='bank_account.currency'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='CurrencyRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coefficient_buy', models.DecimalField(decimal_places=2, max_digits=12)),
                ('coefficient_sell', models.DecimalField(decimal_places=2, max_digits=12)),
                ('currency_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relations_from', to='bank_account.currency')),
                ('currency_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relations_to', to='bank_account.currency')),
            ],
            options={
                'unique_together': {('currency_from', 'currency_to')},
            },
        ),
    ]
