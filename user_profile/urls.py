from django.urls import path
from . import views

urlpatterns = [
    path("profile/", views.user_profile, name="user_profile"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
    path("add-address/", views.add_address, name="add_address"),
    path("saved-address/", views.saved_address, name="saved_address"),
    path("edit-address/<int:eid>", views.edit_address, name="edit_address"),
    path("delete-address/<int:dlid>", views.delete_address, name="delete_address"),
    path("check-password/", views.check_current_password, name="check_current_password"),
    path("update-password/", views.update_password, name="update_password"),
    path("view-coupon/", views.view_coupon, name="view_coupon"),

    path("otp-send/", views.otp_send, name="otp_send"),
    path("otp_verify/", views.otp_verify, name="otp_verify"),
]
