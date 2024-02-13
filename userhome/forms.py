from django import forms
from django.forms import ModelForm
from .models import *
from django.core.validators import RegexValidator, EmailValidator

from allauth.account.forms import SignupForm


class NewUserForm(forms.ModelForm):
    phone_regex = RegexValidator(
        regex=r"^\d{10}$",  # Assuming a 10-digit phone number
        message="Phone number must be a 10-digit number.",
    )

    phone_no = forms.CharField(
        validators=[phone_regex],
        required=True,  # Make the phone number field required
        widget=forms.TextInput(attrs={"placeholder": "Enter your phone number"}),
    )

    email = forms.CharField(
        validators=[EmailValidator(message="Enter a valid email address.")],
        required=True,  # Make the email field required
        widget=forms.EmailInput(attrs={"placeholder": "Enter your email"}),
    )

    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    referal = forms.CharField(
        label="Referal code",
        required=False,  # Make the referal field optional
        widget=forms.TextInput(attrs={"placeholder": "Enter referal code"}),
    )

    class Meta:
        model = NewUser
        fields = ["first_name", "last_name", "email", "phone_no"]
        widgets = {
            "password": forms.PasswordInput(),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.CharField(label="email", max_length=100)
    password = forms.CharField(
        label="password ", max_length=100, widget=forms.PasswordInput()
    )

    class Meta:
        widgets = {
            "password": forms.PasswordInput(),
        }
