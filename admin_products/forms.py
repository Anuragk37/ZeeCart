from django import forms
from django.forms import ModelForm
from .models import *


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"




class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = "__all__"


class ColorForm(forms.ModelForm):
    class Meta:
        model = Color
        fields = "__all__"


class ColorForm(forms.ModelForm):
    class Meta:
        model = Color
        fields = "__all__"


class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        exclude = ["is_deleted", "offer_price"]

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get("price")

        if price is not None and price < 0:
            self.add_error("price", "Price cannot be a negative value.")

        return cleaned_data


class ProductVarientForm(forms.ModelForm):
    class Meta:
        model = ProductVarient
        fields = "__all__"


class ProductOfferForm(forms.ModelForm):
    class Meta:
        model = ProductOffer
        fields = "__all__"

        def clean(self):
            cleaned_data = super().clean()
            discount = cleaned_data.get("discount")

            if discount is not None and discount < 0:
                self.add_error("discount", "discount cannot be a negative value.")

            return cleaned_data


class CategoryOfferForm(forms.ModelForm):
    class Meta:
        model = CategoryOffer
        fields = "__all__"

        def clean(self):
            cleaned_data = super().clean()
            discount = cleaned_data.get("discount")

            if discount is not None and discount < 0:
                self.add_error("discount", "discount cannot be a negative value.")

            return cleaned_data
