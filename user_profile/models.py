from django.db import models

from userhome.models import NewUser


# Create your models here.
class Address(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, related_name="address")
    name = models.CharField(max_length=50, blank=False)
    phone_no = models.CharField(blank=False, max_length=10)
    locality = models.CharField(max_length=255)
    address = models.TextField(blank=False)
    pincode = models.CharField(blank=False)
    city = models.CharField(blank=False)
    state = models.CharField(blank=False)
    alternative_phone_no = models.CharField(blank=True, null=True, max_length=10)

    def __str__(self) -> str:
        return str(self.user)
