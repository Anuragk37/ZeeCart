
from django.shortcuts import redirect, render

from .models import*

from .forms import CouponForm
from datetime import datetime
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required,user_passes_test
from .forms import*
from coupon_banner.models import Banner



# Create your views here.
@login_required(login_url='admin_login')
def coupon(request):
   if request.user.is_admin:
      coupons=Coupon.objects.all().order_by('-id')
      return render(request,'coupon_banner/coupons.html',{'coupons':coupons})
   else:
       return redirect('admin_login')
@login_required(login_url='admin_login')
def add_coupon(request):
   if request.user.is_admin:
      form=CouponForm()
      if request.method=='POST':
         form=CouponForm(request.POST)
         if form.is_valid():
            form.save()
            return redirect('coupon')
      return render(request,'coupon_banner/add-coupon.html',{'form':form})
   return redirect('admin_login')

def apply_coupon(request):
    if request.method == 'POST':
      code = request.POST['code']
      user = request.user
      order_data = request.session.get('cart_data')
      total_price=order_data['total_amount']

      try:
         coupon = Coupon.objects.get(code=code)
         applied_coupon = UserCoupon.objects.filter(user=user)
         current_time = timezone.now()
         
         if coupon.valid_to > current_time and not applied_coupon.filter(coupon=coupon).exists() and total_price> coupon.min_order and coupon.active:
               discount = coupon.discount
               reduced_price=(order_data['total_amount'] * discount) / 100
               order_data['total_amount'] -= (order_data['total_amount'] * discount) / 100
               
               

               request.session['order_data'] = order_data

               UserCoupon.objects.create(user=user, coupon=coupon, is_applyed=True,reduced_price=reduced_price)

               applied_coupon_codes = request.session.get('applied_coupons', [])

                # Add the current applied coupon code to the list
               applied_coupon_codes.append(coupon.code)

                # Store the updated list in the session
               request.session['applied_coupons'] = applied_coupon_codes

               messages.success(request, 'Coupon applied')
               return redirect(reverse('checkout_payment'))
         elif applied_coupon.filter(coupon=coupon).exists():
               messages.error(request, 'Coupon already applied')
         elif coupon.valid_to <= current_time:
               messages.error(request, 'Coupon has expired')
         elif total_price< coupon.min_order:
               messages.error(request, f"the minumun order amount for this coupon is {coupon.min_order}")
         elif not coupon.active:
               messages.error(request, 'Coupon is not available')
         else:
             messages.error(request, 'CSomething went wrong')
      except Coupon.DoesNotExist:
            messages.error(request, 'Invalid coupon code')
            return redirect(reverse('checkout_payment'))
         
    return redirect('checkout_payment')

@login_required(login_url='admin_login')
def activate_coupon(request,coupon_id):
   if request.user.is_admin:
        coupon=Coupon.objects.get(id=coupon_id)
        coupon.active=True
        coupon.save()
        return redirect('coupon')
   else:
      return redirect('admin_login')   
   
@login_required(login_url='admin_login')
def deactivate_coupon(request,coupon_id):
    if request.user.is_admin:
        coupon=Coupon.objects.get(id=coupon_id)
        coupon.active=False
        coupon.save()
        return redirect('coupon')
    else:
      return redirect('admin_login')   

from django.shortcuts import get_object_or_404

def remove_applyed_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        user_coupon = get_object_or_404(UserCoupon, user=request.user, coupon=coupon)

        order_data = request.session.get('cart_data')
        reduced_price=user_coupon.reduced_price
        discount = coupon.discount

        # Check if total_price and discount are not None
        if reduced_price is not None and discount is not None:
            # Add the entire discount back to the total amount
            order_data['total_amount'] += reduced_price
            request.session['order_data'] = order_data

        user_coupon.delete()

        # Retrieve the list of applied coupon codes from the session
        applied_coupon_codes = request.session.get('applied_coupons', [])

        # Remove the current applied coupon code from the list
        applied_coupon_codes.remove(coupon.code)

        # Store the updated list in the session
        request.session['applied_coupons'] = applied_coupon_codes

        messages.success(request, 'Coupon removed successfully')
    except Coupon.DoesNotExist:
        messages.error(request, 'Invalid coupon code')
    except UserCoupon.DoesNotExist:
        messages.error(request, 'Coupon not applied by the user')
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")

    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url='admin_login')
@user_passes_test(lambda u: u.is_admin)
def add_banner(request):
    if request.user.is_authenticated:
        form=BannerForm()
        if request.method=='POST':
            form=BannerForm(request.POST,request.FILES)
            if form.is_valid():
                form.save()
                return redirect('banners')
            else:
                return redirect('add_banner')
        return render(request,'coupon_banner/add-banner.html',{'form':form})
    else:
        messages.error(request,'Your are not an admin')
        return redirect('home')
    
@login_required(login_url='admin_login')
def banners(request):
    if request.user.is_admin:
        banners=Banner.objects.all()
        return render(request,'coupon_banner/banners.html',{'banners':banners})
    else:
      return redirect('admin_login')  
    
@login_required(login_url='admin_login')
def delete_banner(request,bid):
    if request.user.is_admin:
        banner=Banner.objects.get(id=bid)
        banner.delete()
        return redirect('banners')
    else:
      return redirect('admin_login') 

@login_required(login_url="admin_login")
def edit_banner(request, bid):
    if request.user.is_admin:
        banner = Banner.objects.get(id=bid)

        if request.method == "POST":
            form = BannerForm(request.POST, request.FILES, instance=banner)
            if form.is_valid():
                form.save()
                return redirect('banner')
            else:
                return redirect('add_banner')
        else:
            form = BannerForm(instance=banner)
        
        return render(request, "adminhome/add-banner.html", {"form": form})
    else:
        return redirect("admin_login")




