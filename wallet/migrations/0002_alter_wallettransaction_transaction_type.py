# Generated by Django 5.0 on 2024-01-24 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallettransaction',
            name='transaction_type',
            field=models.CharField(choices=[('Deposit', 'Deposit'), ('Withdraw', 'Withdraw'), ('Payment', 'Payment'), ('Refund', 'Refund'), ('Referal', 'Referal'), ('Cashback', 'Cashback')]),
        ),
    ]
