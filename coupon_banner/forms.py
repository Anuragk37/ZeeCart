from django import forms
from django.forms import ModelForm
from .models import*
from coupon_banner.models import*

class CouponForm(forms.ModelForm):
   class Meta:
      model=Coupon
      exclude=['active']
      widgets = {
            'valid_from': forms.TextInput(attrs={'type': 'date'}),
            'valid_to': forms.TextInput(attrs={'type': 'date'}),
        }
      
   def clean(self):
      cleaned_data = super().clean()
      discount = cleaned_data.get('discount')

      if discount is not None and discount < 0:
          self.add_error('discount', 'discount cannot be a negative value.')

      return cleaned_data



class BannerForm(forms.ModelForm):
   class Meta:
        model = Banner
        fields= "__all__"
        widgets = {
            'start_date': forms.TextInput(attrs={'type': 'date'}),
            'end_date': forms.TextInput(attrs={'type': 'date'}),
        }