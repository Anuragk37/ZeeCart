from django import forms
from django.forms import ModelForm
from userhome.models import *
from .models import *
from django.core.validators import RegexValidator


class EditProfileForm(forms.ModelForm):
    phone_regex = RegexValidator(
        regex=r"^\d{10}$", message="Phone number must be a 10-digit number."
    )

    phone_no = forms.CharField(
        validators=[phone_regex],
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Enter your phone number"}),
    )

    class Meta:
        model = NewUser
        exclude = [
            "is_verified",
            "is_active",
            "is_admin",
            "is_staff",
            "last_login",
            "password",
        ]
        widgets = {
            "password": forms.PasswordInput(),
        }
    def save(self, email=None, commit=True):
        instance = super().save(commit=False)

        if email:
            instance.email = email

        if commit:
            instance.save()

        return instance


class AddressForm(forms.ModelForm):
    phone_regex = RegexValidator(
        regex=r"^\d{10}$", message="Phone number must be a 10-digit number."
    )

    # Name validation
    name_validator = RegexValidator(
        regex=r"^[A-Za-z\s]+$", message="Name must only contain letters and spaces."
    )

    name = forms.CharField(
        validators=[name_validator],
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Enter your name"}),
    )

    phone_no = forms.CharField(
        validators=[phone_regex],
        max_length=10,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Enter your phone number"}),
    )

    class Meta:
        model = Address
        exclude = ["user"]
        widgets = {
            "address": forms.Textarea(attrs={"rows": 4}),
        }
