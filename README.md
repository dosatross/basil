This is a personal project to learn new technologies, showcase work and create a custom personal finance analysis solution. The features are centred around my own use cases not generic use cases but may be generalised in the future.

This project uses Django REST Framework to provide a web API for transaction and category data.

### Installation

1. [Install and activate virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtualenv/)

2. `pip install -r requirements.pip`

3. `./manage.py migrate`

### Import CSV Data

Categories:

`./manage import_categories --file <file>`

or ``./manage import_categories` for default file

Transactions:

`./manage import_transactions --transactions <path> --categories_map <path> --source <source>`

or `./manage import_transactions` for defaults

`categories_map` maps categories from a source to basil categories