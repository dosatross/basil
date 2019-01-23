from django.urls import path
from basil.apps.transactions.api import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

urlpatterns = [
    path('income/period/<str:period>', views.IncomePeriodView.as_view(), name='incomeperiod'),
    path('expenses/period/<str:period>', views.ExpensePeriodView.as_view(), name='expenseperiod'),
]

router.register('transactions', views.TransactionsViewSet, basename='transaction')
router.register('expenses', views.ExpensesViewSet, basename='expense')
router.register('income', views.IncomeViewSet, basename='income')

urlpatterns += router.urls