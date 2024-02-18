from django.urls import path
from .import views

urlpatterns = [
    path('products/',views.products, name='products'),
    path('add_products/',views.add_products, name='add_products'),
    path('edit_product/<int:eid>',views.edit_product, name='edit_product'),
    path('delete_product/<int:dlid>',views.delete_product, name='delete_product'),
    path('product_varient/',views.product_varient, name='product_varient'),

    path('offer-management/',views.offer_management,name='offer_management'),
    path('category_offer/',views.category_offer,name='category_offer'),

    path('category/',views.category, name='category'),
    path('add-category/',views.add_category, name='add_category'),
    path('delete_category/<int:dlid>',views.delete_category, name='delete_category'),
    path('edit_category/<int:eid>',views.edit_category, name='edit_category'),

    path('brands/',views.brands, name='brands'),
    path('add-brand/',views.add_brand, name='add_brand'),
    path('delete_brand/<int:bid>',views.delete_brand, name='delete_brand'),
    path('edit-brand/<int:eid>',views.edit_brand, name='edit_brand'),


    path('add_color/',views.add_color, name='add_color'),
    path('delete_color/<int:dlid>',views.delete_color, name='delete_color'),

    path('deleted-products/',views.deleted_products, name='deleted_products'),
    path('retorecategory/<int:product_id>',views.restore_product, name='restore_product'),

    path('product-view/<int:product_id>',views.product_view, name='product_view'),
    path('delete-product-varient/<int:varient_id>',views.delete_product_varient, name='delete_product_varient'),
    path('delete-image/<int:image_id>',views.delete_image, name='delete_image'),





]