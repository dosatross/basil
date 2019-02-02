from django.urls import path
from basil.apps.transactions.api import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

urlpatterns = [
    path('periodtotal/<str:set>/<str:period>', views.PeriodTotalView.as_view(), name='period-total'),
    path('categorytotal/<str:set>', views.CategoryTotalView.as_view(), name='category-total'),
]

router.register('transactions', views.TransactionsViewSet, basename='transaction')
router.register('expenses', views.ExpensesViewSet, basename='expense')
router.register('income', views.IncomeViewSet, basename='income')

urlpatterns += router.urls