from django.shortcuts import redirect, render
from wallet.models import *
from user_order.models import *
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.utils import timezone


# Create your views here.
@login_required(login_url="admin_login")
def view_order_list(request):
    if request.user.is_admin:
        order_list = Order.objects.all().order_by("-id")
        items_per_page = 10
        paginator = Paginator(order_list, items_per_page)
        page = request.GET.get("page")

        try:
            order_list_paginated = paginator.page(page)
        except PageNotAnInteger:
            order_list_paginated = paginator.page(1)
        except EmptyPage:
            order_list_paginated = paginator.page(paginator.num_pages)
        return render(
            request,
            "admin_order_management/order_list.html",
            {"order_list": order_list_paginated},
        )
    else:
        return redirect("admin_login")


@login_required(login_url="admin_login")
def order_details(request, order_id):
    if request.user.is_admin:
        order = Order.objects.get(id=order_id)
        order_products = OrderItems.objects.filter(order=order_id).order_by("id")
        return render(
            request,
            "admin_order_management/order-detail.html",
            {"order_products": order_products, "order": order},
        )
    else:
        return redirect("admin_login")


@login_required(login_url="admin_login")
def update_status(request, orderitem_id):
    if request.user.is_admin:
        if request.method == "POST":
            order_status = request.POST["order-status"]
            order = OrderItems.objects.get(id=orderitem_id)
            order.order_status = order_status
            order.save()
            if order.order_status == "Delivered":
                order.payment_status = "Paid"
                order.delivery_date = timezone.now()
                order.save()
            return redirect(request.META.get("HTTP_REFERER", "/"))


def refund_details(request, orderItem_id):
    order_item = OrderItems.objects.get(id=orderItem_id)
    redund_amount = order_item.quantity * order_item.price
    return render(
        request,
        "admin_order_management/refund.html",
        {"order_item": order_item, "redund_amount": redund_amount},
    )


@login_required(login_url="admin_login")
def refund(request, orderItem_id):
    if request.user.is_admin:
        order_item = OrderItems.objects.get(id=orderItem_id)
        order_item.is_refunded = True

        price = order_item.price
        quantity = order_item.quantity
        amount = price * quantity

        user = order_item.order.user
        wallet = Wallet.objects.get(user=user)
        wallet.balance = wallet.balance + amount

        WalletTransaction.objects.create(
            user=user, wallet=wallet, amount=amount, transaction_type="Refund"
        )

        order_item.save()
        wallet.save()

        order_id = order_item.order.id
        messages.success(request, "refunded")
        return redirect(request.META.get("HTTP_REFERER", "/"))


@login_required(login_url="admin_login")
def return_request_accept(request, orderitem_id):
    if request.user.is_admin:
        item = OrderItems.objects.get(id=orderitem_id)
        item.return_status = "Accepted"
        item.save()
        return redirect(request.META.get("HTTP_REFERER", "/"))
    else:
        return redirect("admin_login")


@login_required(login_url="admin_login")
def return_request_reject(request, orderitem_id):
    if request.user.is_admin:
        item = OrderItems.objects.get(id=orderitem_id)
        item.return_status = "Rejected"
        item.save()
        return redirect(request.META.get("HTTP_REFERER", "/"))
    else:
        return redirect("admin_login")


@login_required(login_url="admin_login")
def return_order(request, orderitem_id):
    if request.user.is_admin:
        item = OrderItems.objects.get(id=orderitem_id)
        item.is_returned = True
        item.save()
        varient = item.product_varient
        varient.stock = varient.stock + item.quantity
        varient.save()
        return refund(request, orderitem_id)
    else:
        return redirect("admin_login")
