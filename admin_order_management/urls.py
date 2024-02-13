from django.urls import path
from .import views

urlpatterns=[
    path('orders/',views.view_order_list, name='view_order_list'),
    path('order-detail/<int:order_id>',views.order_details, name='order_details'),
    path('update-status/<int:orderitem_id>',views.update_status, name='update_status'),

    path('refund/<int:orderItem_id>',views.refund, name='refund'),
    path('refund-details/<int:orderItem_id>',views.refund_details, name='refund_details'),
    
    path('return-request-reject/<int:orderitem_id>',views.return_request_reject, name='return_request_reject'),
    path('return-request-accept/<int:orderitem_id>',views.return_request_accept, name='return_request_accept'),
    path('return-order/<int:orderitem_id>',views.return_order, name='return_order'),

]