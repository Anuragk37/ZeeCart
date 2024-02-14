from django.shortcuts import HttpResponse, redirect
from .models import NewUser
from .views import signout
from django.contrib import messages
from django.contrib.auth import logout


class BlockMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            user = request.user
            if not user.is_active and not user.is_admin:
                logout(request)

        response = self.get_response(request)
        return response
