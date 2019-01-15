from django.urls import path
from basil.apps.transactions.api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('transactions', views.TransactionsViewSet, basename='transactions')
router.register('expenses', views.ExpensesViewSet, basename='expenses')
router.register('income', views.IncomeViewSet, basename='income')

urlpatterns = router.urls