# Generated by Django 3.0.4 on 2020-06-17 10:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transaction_accounts', '0001_initial'),
        ('transactions', '0004_transaction_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='transaction_account',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='transaction_accounts.TransactionAccount'),
        ),
    ]