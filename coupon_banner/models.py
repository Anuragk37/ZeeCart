from django.db import models

from userhome.models import NewUser

# Create your models here.

class Coupon(models.Model):
   code=models.CharField(max_length=10,unique=True)
   discount=models.FloatField()
   valid_from=models.DateTimeField()
   valid_to=models.DateTimeField()
   min_order=models.FloatField()
   active=models.BooleanField(default=True)

   def __str__(self) -> str:
      return self.code
   
class UserCoupon(models.Model):
   user=models.ForeignKey(NewUser,on_delete=models.CASCADE)
   coupon=models.ForeignKey(Coupon,on_delete=models.CASCADE)
   is_applyed=models.BooleanField(default=False)
   reduced_price=models.FloatField()

   def __str__(self) -> str:
      return f"{self.user} -- {self.coupon}"
   

class Banner(models.Model):
    title=models.CharField(default="")
    banner_image=models.ImageField(upload_to='banner_image')
    start_date=models.DateField()
    end_date=models.DateField()
    link=models.CharField(default="")

    

    def __str__(self) -> str:
        return self.title
   
