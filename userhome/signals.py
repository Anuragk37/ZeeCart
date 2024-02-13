from allauth.account.signals import user_logged_in
from django.dispatch import receiver
from .models import NewUser


@receiver(user_logged_in)
def user_logged_in_handler(request, user, **kwargs):

    if user.socialaccount_set.filter(provider="google").exists():

        user.is_verified = True
        user.save()
