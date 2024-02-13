from django.urls import path
from .import views

app_name='wishlist_cart'
urlpatterns = [
    path('cart/',views.cart, name='cart'),
    path('cart-remove/<int:cart_id>/',views.cart_remove, name='cart_remove'),

    path('update-quantity/',views.update_quantity, name='update_quantity'),
    
    path('wishlist/',views.wishlist, name='wishlist'),
    path('wishlist-remove/<int:w_id>/',views.wishlist_remove, name='wishlist_remove'),
   
]