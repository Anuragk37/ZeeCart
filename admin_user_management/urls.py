from django.urls import path
from .import views

urlpatterns = [
    path('view_users/',views.view_users, name='view_users'),
    path('unblock_user/<int:uid>',views.unblock_user, name='unblock_user'),
    path('block_user/<int:uid>',views.block_user, name='block_user'),
    
]