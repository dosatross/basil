import os
import csv
import pytz
import datetime as dt
from django.db.models import Q
from rest_framework.test import APIRequestFactory

from basil.apps.transactions.models import Transaction
from basil.apps.categories.models import Category
from basil.apps.transactions.api.serializers import TransactionSerializer
from basil.settings import BASE_DIR,TIME_ZONE

def import_transactions_csv(user,transactions_csv_path,categories_map_csv_path,source,print_progress=False,replace=False):
  with open(transactions_csv_path) as tf, open(categories_map_csv_path) as cf:
    transactions = csv.DictReader(tf)
    categories_map = csv.DictReader(cf)

    added_transactions = []
    timezone = pytz.timezone(TIME_ZONE)
    
    for transaction in transactions:
      categorystr = transaction['category'].split(" - ")[0]
      subcategory = transaction['category'].split(" - ")[1]
      category = Category.objects.filter(Q(name=categorystr) & Q(subcategory=subcategory) & Q(user=user)).first()

      if not category: # check if a basil category
        for category_map in categories_map:
          # check if a source category
          if not categorystr + subcategory == category_map[source + '_category'] + category_map[source + '_subcategory']:
            print("New category " + categorystr + " - " + subcategory + " detected. New categories must be added before importing transactions.")
            for t in added_transactions:
              t.delete()
            return
          else:
            # get mapped basil category
            categorystr = category_map['basil_category'].split(" - ")[0]
            subcategory = category_map['basil_category'].split(" - ")[1]
            category = Category.objects.filter(Q(name=categorystr) & Q(subcategory=subcategory) & Q(user=user)).first()
            if not category:
              print("New category " + categorystr + " - " + subcategory + " detected. New categories must be added before importing transactions.")
              for t in added_transactions:
                t.delete()
              return
            break


      date = timezone.localize(dt.datetime.strptime(transaction['date'],"%d/%m/%Y"))
      amount = float(transaction['amount'])
      description = transaction['description']

      # validate data
      # mock request to simulate current user
      factory = APIRequestFactory()
      factory = request = factory.get('')
      request.user = user
      context = {"request": request}
      serializer = TransactionSerializer(data={
        'date': date.date(), 'amount': amount,
        'category': category.id,'description': description
        }, context=context)
      if not serializer.is_valid():
        print(serializer.errors)
        for t in added_transactions:
          t.delete()
        return

      
      new_transaction = Transaction.objects.create(date=date,category=category,amount=amount, description=description,user=user)
      added_transactions.append(new_transaction)

      if print_progress:
        print(date)
    if replace:
      Transaction.objects.exclude(pk__in=map(lambda t: t.pk,added_transactions)).delete()

      