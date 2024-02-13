from django.shortcuts import redirect, render
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from userhome.models import NewUser
from .models import *
from admin_products.models import *
from django.db.models import Sum, F
from django.http import JsonResponse


# diplay cart items
def cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart_items = Cart.objects.filter(user=user).order_by("id")
        if cart_items:

            cart_price = (
                cart_items.values("quantity")
                .annotate(
                    total_price=Sum(
                        F("product_varient__product__price") * F("quantity")
                    )
                )
                .aggregate(cart_price=Sum("total_price"))
            )

            discount_price = (
                cart_items.values("quantity")
                .annotate(
                    total_discount=Sum(
                        F("product_varient__product__offer_price") * F("quantity")
                    )
                )
                .aggregate(discount_price=Sum(F("total_discount")))
            )

            discount = cart_price["cart_price"] - discount_price["discount_price"]

            delivery_charge = 0 if cart_price["cart_price"] > 1000 else 100

            total_amount = cart_price["cart_price"] + delivery_charge - discount

            request.session["orginal_cart_amount"] = total_amount

        if cart_items:
            context = {
                "cart_items": cart_items,
                "cart_price": cart_price["cart_price"],
                "delivery_charge": delivery_charge,
                "total_amount": total_amount,
                "discount": discount,
            }
            cart_data = {
                "cart_price": cart_price["cart_price"],
                "discount": discount,
                "delivery_charge": delivery_charge,
                "total_amount": total_amount,
            }
            request.session["cart_data"] = cart_data
        else:
            context = {"cart_items": cart_items}

        return render(request, "wishlist_cart/cart.html", context)
    else:
        return redirect("home")


# updating the cart


def update_quantity(request):
    try:
        product_varient_id = request.GET.get("product_id")
        quantity_no = int(request.GET.get("quantity"))
        user = request.user

        if product_varient_id and quantity_no:
            product_varient = ProductVarient.objects.get(id=product_varient_id)
            cart_item = Cart.objects.get(
                product_varient__id=int(product_varient_id), user=user
            )
            cart_item.quantity = quantity_no

            cart_item.save()

            print(
                f"Updated quantity to {quantity_no} for cart item with ID {cart_item.id}"
            )

        cart_products = Cart.objects.filter(user=user)
        cart_price = (
            cart_products.values("quantity")
            .annotate(
                total_price=Sum(F("product_varient__product__price") * F("quantity"))
            )
            .aggregate(cart_price=Sum("total_price"))
        )

        discount_price = (
            cart_products.values("quantity")
            .annotate(
                total_discount=Sum(
                    F("product_varient__product__offer_price") * F("quantity")
                )
            )
            .aggregate(discount_price=Sum(F("total_discount")))
        )

        discount = int(cart_price["cart_price"] - discount_price["discount_price"])
        total_amount = cart_price["cart_price"] - discount

        response = {
            "cart_price": cart_price["cart_price"],
            "discount": discount,
            "total_amount": total_amount,
            "stock": product_varient.stock,
        }

        request.session["cart_data"] = response
        print(f"Response: {response}")

        return JsonResponse(response)
    except Exception as e:
        print(f"Error in update_quantity view: {e}")
        return JsonResponse({"error": "An error occurred"})


# remove items from the cart
@login_required(login_url="signin")
def cart_remove(request, cart_id):
    cart_item = Cart.objects.get(id=cart_id)
    cart_item.delete()
    return redirect("wishlist_cart:cart")


# display wishlist
def wishlist(request):
    if request.user.is_authenticated:
        user = request.user
        wishlist_items = Wishlist.objects.filter(user=user).order_by("id")
        return render(
            request, "wishlist_cart/wishlist.html", {"wishlist_items": wishlist_items}
        )
    else:
        return redirect("signin")


# remove form wishlist
@login_required(login_url="signin")
def wishlist_remove(request, w_id):
    wishlist_item = Wishlist.objects.filter(product__id=w_id)
    wishlist_item.delete()
    messages.success(request, "Removed from wishlist")
    return redirect(request.META.get("HTTP_REFERER", "/"))
