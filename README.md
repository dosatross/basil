This is a personal project to learn new technologies, showcase work and create a custom personal finance analysis solution. The features are centred around my own use cases not generic use cases but may be generalised in the future.

This project uses Django REST Framework to provide a web API for transaction and category data.

### Installation

1. [Install and activate virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtualenv/)

2. `pip install -r requirements.pip`

3. `python ./manage.py migrate`

### Import Data

1. Category groups: `python ./manage.py import_groups --file <file> --username <username>`
2. Categories: `python ./manage.py import_categories --file <file> --username <username>`
3. Transactions: `python ./manage.py import_transactions --transactions <path> --categories_map <path> --source <source> --username <username>`

`categories_map` maps categories from a source to basil categories

Running commands without parameters will import sample data

`python ./manage.py import_users` imports a default superuser, admin and application user: 'su', 'admin', 'demo' (same username and password)



