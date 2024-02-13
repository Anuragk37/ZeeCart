from django import forms
from .models import Order

class PaymentMethodForm(forms.ModelForm):
   class Meta:
      model = Order
      fields = ['payment_method']
      widgets = {
            'payment_method': forms.RadioSelect(attrs={'class': 'payment-method-radio'}),
        }

   def __init__(self, *args, **kwargs):
      super(PaymentMethodForm, self).__init__(*args, **kwargs)
      self.fields['payment_method'].choices = Order.PAYMENT_METHOD_CHOICES
      self.fields['payment_method'].empty_label = None
