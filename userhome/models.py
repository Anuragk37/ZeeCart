from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.crypto import get_random_string


# Create your models here.jffu  nudncn8n n uc jenjcn incn    p a pef nne if en viroin
class NewUserManager(BaseUserManager):
    def create_user(self, first_name, last_name, phone_no, email, password=None):
        if not email:
            raise ValueError("user must have an email address")
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone_no=phone_no,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, phone_no, email, password=None):
        user = self.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_no=phone_no,
        )
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class NewUser(AbstractBaseUser):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone_no = models.CharField(unique=True, max_length=10)
    email = models.EmailField(unique=True, max_length=255)
    referal_code = models.CharField(unique=True, max_length=8, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    objects = NewUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone_no"]

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):
        self.referal_code = get_random_string(length=8)
        super().save(*args, **kwargs)
