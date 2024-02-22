from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from wallet.models import *
from userhome import context_processors
from coupon_banner.models import Banner, Coupon
from .models import *
from .forms import *
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
import random
from admin_products.models import *
from django.contrib.auth.decorators import login_required


# Create your views here.


# home page
def home(request):
    brands = Brand.objects.filter(is_deleted=False)
    categories = Category.objects.filter(is_deleted=False)
    products = Products.objects.all().order_by("-created_at")
    banners = Banner.objects.all()
    coupons = Coupon.objects.all()
    return render(
        request,
        "userhome/index.html",
        {
            "brands": brands,
            "categories": categories,
            "products": products,
            "banners": banners,
            "coupons": coupons,
        },
    )


def signup(request):
    if not request.user.is_authenticated:
        form = NewUserForm()
        if request.method == "POST":
            form = NewUserForm(request.POST)
            if form.is_valid():
                try:
                    user = form.save(commit=False)
                    user.is_verified = False
                    user.save()
                    email = form.cleaned_data.get("email")
                    request.session["email"] = email
                    referal = form.cleaned_data.get("referal")
                    request.session["referal"] = referal
                    return send_otp(request)

                except Exception as e:
                    messages.error(request, f"Error: {e}")
                    return redirect("signup")

        return render(request, "userhome/signup.html", {"form": form})
    else:
        return redirect("home")


def send_otp(request):
    otp = str(random.randint(100000, 999999))
    email = request.session.get("email")
    subject = "OTP Verification"
    message = f"This is your OTP: {otp}"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]

    send_mail(subject, message, email_from, recipient_list)

    request.session["otp"] = otp

    return redirect("verify_otp")


def resend_otp(request):

    messages.success(request, "an otp has been sended to the email")
    return send_otp(request)


def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST["entered_otp"]
        try:
            if entered_otp == request.session["otp"]:

                user = NewUser.objects.get(email=request.session.get("email"))
                user.is_verified = True
                user.save()

                if request.session.get("referal"):
                    referal = request.session.get("referal")
                    referal_user = NewUser.objects.get(referal_code=referal)
                    referal_user_wallet = Wallet.objects.get(user=referal_user)
                    referal_user_wallet.balance += 500
                    referal_user_wallet.save()
                    WalletTransaction.objects.create(
                        user=referal_user,
                        wallet=referal_user_wallet,
                        amount=500,
                        transaction_type="Referal",
                    )

                    wallet = Wallet.objects.get(user=user)
                    wallet.balance += 200
                    wallet.save()
                    WalletTransaction.objects.create(
                        user=user,
                        wallet=wallet,
                        amount=200,
                        transaction_type="Cashback",
                    )

                del request.session["otp"]

                messages.success(request, "Account successfully verified.")
                return redirect("home")
            else:
                messages.error(request, "Invalid OTP. Please try again.")
                return redirect(reverse("verify_otp"))
        except Exception as e:
            messages.error(request, f"Error On: {e}")
            return redirect(reverse("verify_otp"))

    return render(request, "userhome/verify-otp.html")


def signin(request):
    if not request.user.is_authenticated:
        form = LoginForm()
        if request.method == "POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get("email")
                password = form.cleaned_data.get("password")
                user = authenticate(request, email=email, password=password)
                if user is not None and not user.is_admin:
                    if not user.is_active:
                        messages.error(request, "you are blocked , so you cant log in")
                        return redirect("signin")
                    elif not user.is_verified:
                        messages.error(
                            request, "your account is not verified , so you cant log in"
                        )
                        return redirect("signin")
                    else:
                        login(request, user)
                        messages.success(request, "You are logged in.")
                        return redirect("home")
                else:
                    messages.error(request, "Invalid credentials. Please try again.")
                    return redirect("signin")
        return render(request, "userhome/signin.html", {"form": form})
    else:
        return redirect("home")


def signout(request):
    logout(request)
    return redirect("home")


def forgott_password(request):
    if request.method == "POST":
        email = request.POST["email"]
        user = NewUser.objects.get(email=email)
        if user:
            otp = str(random.randint(100000, 999999))
            subject = "otp varification for updating password"
            message = f"this is your otp : {otp}"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, email_from, recipient_list)

            request.session["pass-email"] = email
            request.session["forgot-otp"] = otp

            messages.success(request, "An OTP has been sent to your email.")
            return redirect("otp_forgot_password")
        else:
            messages.error(request, "User with this email does not exist.")
            return redirect(reverse("forgott_password"))

    return render(request, "userhome/forgot-password.html")


def otp_forgot_password(request):
    if request.method == "POST":
        entered_otp = request.POST["entered_otp"]
        if entered_otp == request.session["forgot-otp"]:
            del request.session["forgot-otp"]
            messages.success(request, "you can change your password here ")
            return redirect("password_update")
        else:
            messages.error(request, "Invalid OTP. Please try again.")
    return render(request, "userhome/otp-forgot-password.html")


def password_update(request):
    if request.method == "POST":
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 == password2:
            user = NewUser.objects.get(email=request.session.get("pass-email"))
            user.set_password(password1)
            user.save()
            del request.session["pass-email"]
            messages.success(request, "your password has been updated ")
            return redirect("signin")
        else:
            messages.success(request, "password mismatch ")
            return redirect(reverse("password_update"))

    return render(request, "userhome/update-password.html")
