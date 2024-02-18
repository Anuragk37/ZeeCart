from django.http import JsonResponse
from django.shortcuts import redirect, render
import razorpay

from .models import *
from userhome.models import *
from django.contrib import messages

from django.conf import settings

# Create your views here.


# wallet view
def wallet(request):
    if request.user.is_authenticated:
        user = request.user
        wallet = Wallet.objects.get(user=user)
        return render(request, "wallet/wallet.html", {"wallet": wallet})
    else:
        return redirect("signin")


# add amount function
def add_amount(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            amount = int(request.POST["amount"])

            user = request.user
            wallet = Wallet.objects.get(user=user)
            wallet.balance += amount
            wallet.save()

            WalletTransaction.objects.create(
                user=user, wallet=wallet, amount=amount, transaction_type="Deposit"
            )

        return JsonResponse({"message": "amount added successfully"})

    else:
        return redirect("signin")


# withdraw
def withdraw(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            amount = float(request.POST["amount"])
            user = request.user
            wallet = Wallet.objects.get(user=user)

            if wallet.balance >= amount:
                wallet.balance -= amount
                wallet.save()
                WalletTransaction.objects.create(
                    user=user, wallet=wallet, amount=amount, transaction_type="Withdraw"
                )
            else:
                messages.success(request, "Insufficient balance")
                return redirect("wallet")

        return redirect("wallet")
    else:
        return redirect("signin")


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from .models import WalletTransaction


def transaction_history(request):
    if request.user.is_authenticated:
        user = request.user
        wallet = Wallet.objects.get(user=user)
        transactions = WalletTransaction.objects.filter(wallet=wallet).order_by("-id")

        transactions_per_page = 15
        paginator = Paginator(transactions, transactions_per_page)

        page = request.GET.get("page")
        try:
            transactions = paginator.page(page)

        except PageNotAnInteger:
            transactions = paginator.page(1)

        except EmptyPage:
            transactions = paginator.page(paginator.num_pages)

        return render(
            request, "wallet/transactions.html", {"transactions": transactions}
        )
