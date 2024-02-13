from django.urls import path
from .import views

urlpatterns = [
   path('checkout-address/', views.checkout_address, name='checkout_address'),
   path('checkout-payment/', views.checkout_payment, name='checkout_payment'),
   path('cash-on-delivery/', views.cash_on_delivery, name='cash_on_delivery'),
   path('wallet-payment/', views.wallet_payment, name='wallet_payment'),
   path('online-payment/', views.online_payment, name='online_payment'),


   path('razorpay-check/', views.razorpay_check, name='razorpay_check'),

   path('order-list/',views.order_list, name='order_list'),

   # path('checkout-product/<int:varient_id>',views.single_product_order, name='single_product_order'),
   # path('quantity-update/',views.quantity_update, name='quantity_update'),

   path('cancel-order/<int:orderitem_id>',views.cancel_order, name='cancel_order'),
   path('order-detail/<int:orderitem_id>',views.order_detail, name='order_detail'),
   path('return-request/<int:orderitem_id>',views.return_request, name='return_request'),
   path('invoice-pdf/<int:orderitem_id>',views.invoice_pdf, name='invoice_pdf'),
]