from django import forms
from django.forms import ModelForm
from coupon_banner.models import*

class BannerForm(forms.ModelForm):
   class Meta:
        model = Banner
        fields= "__all__"
        widgets = {
            'start_date': forms.TextInput(attrs={'type': 'date'}),
            'end_date': forms.TextInput(attrs={'type': 'date'}),
        }
