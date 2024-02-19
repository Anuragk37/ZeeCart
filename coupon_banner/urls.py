from django.urls import path
from . import views

urlpatterns = [
   path('coupon/',views.coupon, name='coupon'),
   path('add_coupon/',views.add_coupon, name='add_coupon'),
   path('apply-coupon/',views.apply_coupon, name='apply_coupon'),

   path('activate-coupon/<int:coupon_id>',views.activate_coupon, name='activate_coupon'),
   path('deactivate-coupon/<int:coupon_id>',views.deactivate_coupon, name='deactivate_coupon'),
   path('remove_applyed_coupon/<str:code>',views.remove_applyed_coupon, name='remove_applyed_coupon'),

   path('add-banner/',views.add_banner, name='add_banner'),
   path('banners/',views.banners, name='banners'),
   path('delete-banner/<int:bid>',views.delete_banner, name='delete_banner'),
   path('edit-banner/<int:bid>',views.edit_banner, name='edit_banner'),
]