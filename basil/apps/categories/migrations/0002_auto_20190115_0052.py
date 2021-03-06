# Generated by Django 2.1.5 on 2019-01-14 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='is_adjustment',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='category',
            name='is_credit',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='is_earned',
            field=models.BooleanField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='is_internal',
            field=models.BooleanField(default=False),
        ),
    ]
