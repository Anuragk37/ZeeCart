from .models import NewUser


def user_context(request):
    email = request.session.get("uid")
    if email:
        customer = NewUser.objects.get(email=email)
    else:
        customer = None

    return {"customer": customer}
