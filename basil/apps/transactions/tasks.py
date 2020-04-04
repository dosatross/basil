import os
from basil.celery import app

from basil.settings import UPLOAD_DATA_DIR, DATA_DIR
from basil.apps.accounts.models import BasilUser
from basil.apps.transactions.models import Transaction
from basil.apps.transactions.services import import_transactions_csv

IMPORT_TRANSACTIONS_CSV_TASK = 'basil.transactions.tasks.import_transactions_csv_task'

@app.task(name=IMPORT_TRANSACTIONS_CSV_TASK,bind=True)
def import_transactions_csv_task(self,user_id, file_name, replace=False):
  source = 'pb'
  user = BasilUser.objects.get(id=user_id)
  transactions_csv_path = os.path.join(UPLOAD_DATA_DIR,file_name)
  categories_map_csv_path = os.path.join(DATA_DIR,'categories_map.csv')
  import_transactions_csv(user,transactions_csv_path,categories_map_csv_path,source, replace=replace)
  