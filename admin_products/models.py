from collections.abc import Iterable
from django.utils import timezone
from django.db import models

from django.dispatch import receiver
from django.db.models.signals import post_save

from django.core.validators import MinValueValidator

# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=200, unique=True)
    category_image = models.ImageField(upload_to="category-images/")
    is_deleted=models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.category_name


class Brand(models.Model):
    brand_name = models.CharField(max_length=200, unique=True)
    brand_image = models.ImageField(upload_to="brand_image/")
    is_deleted=models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.brand_name


class Color(models.Model):
    color = models.CharField(max_length=200, unique=True)

    def __str__(self) -> str:
        return self.color


class Products(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    offer_price = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.product_name

    def save(self, *args, **kwargs):
        if not self.offer_price:
            categroy_offer_exist = CategoryOffer.objects.filter(
                category=self.category
            ).exists()

            if categroy_offer_exist:
                categroy_offer = CategoryOffer.objects.get(category=self.category)
                self.offer_price = (
                    self.price - (categroy_offer.discount * self.price) / 100
                )
            else:
                self.offer_price = self.price
        super().save(*args, **kwargs)


class ProductVarient(models.Model):
    product = models.ForeignKey(
        Products, on_delete=models.CASCADE, related_name="product_varient"
    )
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.product.product_name} - {self.color.color}"


class ProductImage(models.Model):
    product_varient = models.ForeignKey(
        ProductVarient, on_delete=models.CASCADE, related_name="product_images"
    )
    image = models.ImageField(upload_to="product_image/")


class ProductOffer(models.Model):
    product = models.ForeignKey(
        Products, on_delete=models.CASCADE, related_name="offer"
    )
    discount = models.FloatField(default=0, validators=[MinValueValidator(0)])
    is_active=models.BooleanField(default=True)


class CategoryOffer(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="category_offer"
    )
    discount = models.FloatField(default=0, validators=[MinValueValidator(0)])
    is_active=models.BooleanField(default=True)
