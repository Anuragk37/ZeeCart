from django.db import models
from admin_products.models import ProductVarient
from user_profile.models import Address

from userhome.models import NewUser

# Create your models here.

class OrderAddress(models.Model):
   name=models.CharField(max_length=50,blank=False)
   phone_no=models.CharField(blank=False,max_length=10)
   locality=models.CharField(max_length=255)
   address=models.TextField(blank=False)
   pincode=models.CharField(blank=False)
   city=models.CharField(blank=False)
   state=models.CharField(blank=False)
   alternative_phone_no=models.CharField(blank=True,null=True,max_length=10)

   def __str__(self):
      return str(self.id)

class Order(models.Model):
   
   PAYMENT_METHOD_CHOICES = [
        ('Cash_on_Delevery', 'Cash on Delevery'),
        ('Online_Payment', 'Online payment'),
        ('Wallet', 'Wallet'),
    ]
   user=models.ForeignKey(NewUser,on_delete=models.CASCADE)
   address=models.ForeignKey(OrderAddress,on_delete=models.CASCADE)
   payment_method=models.CharField(choices=PAYMENT_METHOD_CHOICES)
   order_date=models.DateTimeField(auto_now_add=True)
   total_amount = models.FloatField()
   
   
   
 
   def __str__(self) -> str:
      return f"{self.user.first_name}-{self.id}"
   
class OrderItems(models.Model):
   ORDER_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed','Confirmed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Canceled','Canceled')
    ]
   
   PAYMENT_STATUS_CHOICES = [
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
        ('Failed', 'Failed'),
    ]
   
   RETURN_STATUS_CHOICES = [
        ('Request', 'Request'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]
   order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='order_items')
   product_varient=models.ForeignKey(ProductVarient,on_delete=models.CASCADE)
   price=models.FloatField()
   quantity=models.PositiveBigIntegerField()
   order_status=models.CharField(max_length=50,choices=ORDER_STATUS_CHOICES, default='Pending')
   payment_status = models.CharField(max_length=50 , choices=PAYMENT_STATUS_CHOICES, default='Pending')
   delivery_date = models.DateTimeField(null=True, blank=True)
   is_refunded=models.BooleanField(default=False)
   return_status=models.CharField(max_length=50,choices=RETURN_STATUS_CHOICES,null=True, blank=True)
   is_returned=models.BooleanField(default=False)

   def __str__(self) -> str:
      return str(self.order.id)

class Payment(models.Model):
   PAYMENT_METHOD_CHOICES = [
        ('Cash_on_Delevery', 'Cash on Delevery'),
        ('Razorpay', 'Razorpay'),
        ('PayPal', 'PayPal'),
        ('Wallet', 'Wallet'),
    ]
   order=models.ForeignKey(Order,on_delete=models.CASCADE)
   amount=models.FloatField()
   payment_method = models.CharField(choices=PAYMENT_METHOD_CHOICES,max_length=50)
   date=models.DateTimeField(auto_now_add=True)
   razorpay_payment_id=models.CharField(null=True, blank=True)
   

