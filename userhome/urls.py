from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("signin/", views.signin, name="signin"),
    path("signout/", views.signout, name="signout"),
    path("verify_otp/", views.verify_otp, name="verify_otp"),
    path("resend-otp/", views.resend_otp, name="resend_otp"),
    path("forgott-password/", views.forgott_password, name="forgott_password"),
    path("otp_forgot_password/", views.otp_forgot_password, name="otp_forgot_password"),
    path("password-update/", views.password_update, name="password_update"),
]
