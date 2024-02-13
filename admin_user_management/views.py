from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from userhome.models import NewUser

# Create your views here.
@login_required(login_url='admin_login')
def view_users(request):
    if request.user.is_admin:
        users=NewUser.objects.exclude(is_admin=True)
        return render(request,'admin_user_management/view-user.html',{'users':users})
    else:
        return redirect('admin_login')

@login_required(login_url='admin_login')
def block_user(request,uid):
    if request.user.is_admin:
        user=NewUser.objects.get(id=uid)
        user.is_active=False
        user.save()
        return redirect('view_users')
    else:
        return redirect('admin_login')

@login_required(login_url='admin_login')
def unblock_user(request,uid):
    if request.user.is_admin:
        user=NewUser.objects.get(id=uid)
        user.is_active=True      
        user.save()
        return redirect('view_users')
    else:
        return redirect('admin_login')
    
