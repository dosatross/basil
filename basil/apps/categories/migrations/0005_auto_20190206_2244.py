# Generated by Django 2.1.5 on 2019-02-06 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0004_auto_20190123_1413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorygroup',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]