from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login
from coupon_banner.models import Coupon

from user_order.models import OrderItems
from .forms import *

from userhome.models import *


# Create your views here.
@login_required(login_url="signin")
def user_profile(request):
    user = request.user
    return render(request, "user_profile/profile.html", {"user": user})


@login_required(login_url="signin")
def edit_profile(request):
    user = request.user
    form = EditProfileForm(instance=user)
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("user_profile")

    return render(request, "user_profile/edit-profile.html", {"form": form})


@login_required(login_url="signin")
def add_address(request):
    form = AddressForm()
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            if "from_checkout" in request.GET:
                return redirect("checkout_address")
            else:
                return redirect("saved_address")
    return render(request, "user_profile/add-address.html", {"form": form})


@login_required(login_url="signin")
def saved_address(request):
    user = request.user
    addresses = Address.objects.filter(user=user)
    return render(request, "user_profile/saved-address.html", {"addresses": addresses})


@login_required(login_url="signin")
def edit_address(request, eid):
    address = Address.objects.get(id=eid)
    form = AddressForm(instance=address)
    if request.method == "POST":
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect("saved_address")
    return render(request, "user_profile/edit-address.html", {"form": form})


@login_required(login_url="signin")
def delete_address(request, dlid):
    address = Address.objects.get(id=dlid)
    address.delete()
    return redirect("saved_address")


@login_required(login_url="signin")
def check_current_password(request):
    if request.method == "POST":
        entered_password = request.POST["password"]
        user = request.user

        if check_password(entered_password, user.password):
            return redirect("update_password")
        else:
            messages.error(request, "Password is not correct ")

    return render(request, "user_profile/check-password.html")


@login_required(login_url="signin")
def update_password(request):
    if request.method == "POST":
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        user = request.user

        if password1 == password2:
            user.set_password(password1)
            user.save()
            login(request, user)
            messages.success(request, "Password updated successfully")
            return redirect("user_profile")
        else:
            messages.error(request, "Password mismatch ")

    return render(request, "user_profile/update-password.html")


def view_coupon(request):
    coupons = Coupon.objects.all()
    return render(request, "user_profile/coupons.html", {"coupons": coupons})
