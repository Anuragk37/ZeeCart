from django.db import models

# Create your models here.
from django.db import models
from admin_products.models import ProductVarient, Products
from userhome.models import NewUser


# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, related_name="carts")
    product_varient = models.ForeignKey(ProductVarient, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.first_name}'s Cart - {self.product_varient.product.product_name}"


class Wishlist(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, related_name="wishlist")
    product = models.ForeignKey(Products, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.first_name}'s Wishlist - {self.product.product_name}"
