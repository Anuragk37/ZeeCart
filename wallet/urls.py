from django.urls import path
from .import views

urlpatterns = [
    path('wallet/',views.wallet, name='wallet'),   
    path('add-amount/',views.add_amount, name='add_amount'),
    path('withdraw/',views.withdraw, name='withdraw'),
    path('transactions/',views.transaction_history, name='transaction_history'),
]