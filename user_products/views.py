from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.contrib import messages
from userhome.context_processors import user_context
from django.contrib.auth.decorators import login_required

from admin_products.models import *
from wishlist_cart.models import *
from userhome.models import *


# Create your views here.
def products_list(request, type=None, id=None):
    if type == 'brand':
        print("Brand")
        products = Products.objects.filter(brand__id=id, is_deleted=False)
        categories = Category.objects.all()
        brands = None
    elif type == 'category':
        print("Category")
        products = Products.objects.filter(category__id=id, is_deleted=False)
        brands = Brand.objects.all()
        categories = None
    else:
        products = Products.objects.filter(is_deleted=False)
        categories = Category.objects.all()
        brands = Brand.objects.all()

    context = {"products": products, "categories": categories, "brands": brands}

    if request.user.is_authenticated:
        user = request.user
        wishlist_items = user.wishlist.all()
        wishlist_products = [items.product for items in wishlist_items]

        context["wishlist_products"] = wishlist_products

    return render(request, "user_products/products-list.html", context)



def product_detail(request, pid):
    product = Products.objects.get(id=pid)
    product_varients = product.product_varient.all()
    category = product.category
    similar_products = Products.objects.filter(category=category)
    # user=NewUser.objects.get(email=request.session.get('uid'))
    cart_item = Cart.objects.filter()
    images = [varient.product_images.all() for varient in product_varients]

    # price=product.price
    # discount=price-product.offer.first().discount_price
    # total_amount=price-discount

    # product_data={
    #     'price':price,
    #     'discount':discount,
    #     'total_amount':total_amount
    # }

    # request.session['product_data']=product_data

    return render(
        request,
        "user_products/product-details.html",
        {
            "product": product,
            "product_varient": product_varients,
            "product_images": images,
            "cart_item": cart_item,
            "similar_products": similar_products,
        },
    )


def filter_products(request):
    categories = request.GET.getlist("category[]")
    brands = request.GET.getlist("brand[]")
    low_price = request.GET.get("low_price")
    high_price = request.GET.get("high_price")
    discount = request.GET.get("discount")

    products = Products.objects.filter(is_deleted=False)

    if len(categories) > 0:
        products = products.filter(category__id__in=categories, is_deleted=False)
    if len(brands) > 0:
        products = products.filter(brand__id__in=brands, is_deleted=False)
    if low_price and high_price:
        products = products.filter(
            price__range=(low_price, high_price), is_deleted=False
        )
    if discount:
        products = products.filter(offer__discount__gt=discount, is_deleted=False)

    data = render_to_string("ajax_templates/product-list.html", {"products": products})
    return JsonResponse({"data": data})


@login_required(login_url="signin")
def add_cart(request, pid):
    product_varient = ProductVarient.objects.get(id=pid)
    print(product_varient)
    user = request.user
    cart_item, created = Cart.objects.get_or_create(
        user=user, product_varient=product_varient
    )
    if not created:
        messages.success(request, "Aitem is already in the cart")
        return redirect(request.META.get("HTTP_REFERER", "/"))
    return redirect("wishlist_cart:cart")


@login_required(login_url="signin")
def add_wishlist(request, pid):
    if request.user.is_authenticated:
        product = Products.objects.get(id=pid)
        user = request.user
        wislist_item, created = Wishlist.objects.get_or_create(
            user=user, product=product
        )
        if not created:
            messages.success(request, "Aitem is already in the wishlist")
            return redirect(request.META.get("HTTP_REFERER", "/"))
        else:
            messages.success(request, "Added to wishlist")
            return redirect(request.META.get("HTTP_REFERER", "/"))
    else:
        return redirect(request.META.get("HTTP_REFERER", "/"))


def search_products(request):
    if request.method == "POST":
        name = request.POST["name"]
        products = Products.objects.filter(product_name__icontains=name)
        brands = Brand.objects.all()
        categories = Category.objects.all()
        return render(
            request,
            "user_products/products-list.html",
            {"products": products, "brands": brands, "categories": categories},
        )


def sort_products(request):
    sort_id = request.GET.get("sort_param")

    if sort_id == "1":
        products = Products.objects.all().order_by("price")  # Ascending order
    elif sort_id == "2":
        products = Products.objects.all().order_by("-price")  # Descending order
    else:
        products = Products.objects.all()  # Default order (you can modify this)

    print(sort_id)
    data = render_to_string("ajax_templates/product-list.html", {"products": products})
    return JsonResponse({"data": data})
