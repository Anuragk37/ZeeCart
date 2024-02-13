from django.urls import path
from . import views

app_name = "user_products"

urlpatterns = [
    path("products_list/<int:bid>", views.products_list, name="brand_products"),
    path("products_list/<int:cid>", views.products_list, name="category_products"),
    path("products_list/", views.products_list, name="products_list"),
    path("product_detail/<int:pid>", views.product_detail, name="product_detail"),
    path("filter-products/", views.filter_products, name="filter_products"),
    path("add-cart/<int:pid>", views.add_cart, name="add_cart"),
    path("add-wishlist/<int:pid>", views.add_wishlist, name="add_wishlist"),
    path("search-products/", views.search_products, name="search_products"),
    path("sort-products/", views.sort_products, name="sort_products"),
]
