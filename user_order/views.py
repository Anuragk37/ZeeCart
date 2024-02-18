from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from coupon_banner.models import Coupon,UserCoupon
from wallet.models import *
from wishlist_cart.models import Cart
from .models import*
from.forms import PaymentMethodForm
from user_profile.models import Address
from django.contrib import messages
from django.views.decorators.cache import never_cache,cache_control
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from userhome.models import NewUser
import razorpay 
from django.utils import timezone

from django.db.models import Sum






# Create your views here.
@never_cache
def checkout_address(request):
   if request.user.is_authenticated:
      user=request.user
      addresses=Address.objects.filter(user=user)
      order_data=request.session.get('cart_data')
      request.session['order_data']=order_data
      cart_items=Cart.objects.filter(user=user)
      for item in cart_items:
         if item.quantity>item.product_varient.stock:
            messages.error(request, f"{item.product_varient.product.product_name} {item.product_varient.color} is out of stock")
            return redirect('wishlist_cart:cart')

      return render(request,'user_order/checkout-address.html',{'addresses':addresses,'order_data':order_data})
   else:
      return redirect('signin')

@never_cache
@login_required(login_url='signin')
def checkout_payment(request):
   if request.method == 'POST':
      address_id=request.POST['address']
      request.session['selected-address']=address_id      
      price=request.session.get('order_data')['total_amount']

   order_data=request.session.get('order_data')

   form=PaymentMethodForm()

   coupons = request.session.get('applied_coupons', [])
   coupon_discount=0
   if request.session.get('applied_coupons'):
      applied_coupons=request.session.get('applied_coupons')
      for coupon in applied_coupons:
         c=Coupon.objects.get(code=coupon)
         used_coupon=UserCoupon.objects.get(user=request.user,coupon=c.id)
         coupon_discount=coupon_discount+used_coupon.reduced_price

   return render(request,'user_order/checkout-payment.html',{'form':form,'order_data':order_data,'coupons':coupons,'coupon_discount':coupon_discount})
       
# @login_required(login_url='signin')
# def payment_options(request):
#    if request.user.is_authenticated:
#       user=request.user
#       address_id=request.session.get('selected-address')

#       address=Address.objects.get(id=address_id)
#       total_amount=request.session['order_data']['total_amount']
#       order_items=Cart.objects.filter(user=user)
#       if request.method== 'POST':
#          form = PaymentMethodForm(request.POST)
#          if form.is_valid():
#             payment_method=form.cleaned_data.get('payment_method')   
#             if payment_method=='Cash_on_Delevery':
#                return cash_on_delivery(request,total_amount,user,order_items,address)

#             elif payment_method=='Wallet':
#                return wallet_payment(request,total_amount,user,order_items,address)
#    else:
#       return redirect('signin')
   
@login_required(login_url='signin')
def cash_on_delivery(request):
   try: 
      user=request.user
      address_id=request.session.get('selected-address')
      selected_address=Address.objects.get(id=address_id)
      total_amount=request.session['order_data']['total_amount']
      order_items=Cart.objects.filter(user=user)

      name=selected_address.name
      order_address=selected_address.address
      phone_no=selected_address.phone_no
      pincode=selected_address.pincode
      city=selected_address.city
      state=selected_address.state
      alternative_phone_no=selected_address.alternative_phone_no

      address=OrderAddress.objects.create(name=name,address=order_address,phone_no=phone_no,pincode=pincode,
                                          city=city,state=state,alternative_phone_no=alternative_phone_no)

      order=Order.objects.create(user=user,address=address,payment_method='Cash_on_Delevery',total_amount=total_amount)
      for item in order_items:
         price=item.product_varient.product.offer_price
         OrderItems.objects.create(order=order,product_varient=item.product_varient,price=price,quantity=item.quantity)
         product_varient=item.product_varient
         product_varient.stock=product_varient.stock-item.quantity
         product_varient.save()
         
      cart_items=Cart.objects.filter(user=user)
      cart_items.delete()
      del request.session['selected-address']
      del request.session['cart_data']
      messages.success(request, 'order placed successfully')
      return render(request,'user_order/success.html',{'address':address,'order_items':order_items,'total_amount':total_amount,'payment_method':'Cash_on_delivery'})
   except Exception as e:
      messages.error(request, f'Error placing order: {str(e)}')
      return redirect('checkout_payment') 

@login_required(login_url='signin')
def wallet_payment(request):
   try:
      user=request.user
      wallet=Wallet.objects.get(user=user)
      total_amount=request.session['order_data']['total_amount']
      if wallet.balance>total_amount:
         wallet.balance -= total_amount
         wallet.save()

         address_id=request.session.get('selected-address')
         selected_address=Address.objects.get(id=address_id)
         order_items=Cart.objects.filter(user=user)

         name=selected_address.name
         order_address=selected_address.address
         phone_no=selected_address.phone_no
         pincode=selected_address.pincode
         city=selected_address.city
         state=selected_address.state
         alternative_phone_no=selected_address.alternative_phone_no

         address=OrderAddress.objects.create(name=name,address=order_address,phone_no=phone_no,pincode=pincode,
                                             city=city,state=state,alternative_phone_no=alternative_phone_no)
         order=Order.objects.create(user=user,address=address,payment_method='Wallet',total_amount=total_amount)

         for item in order_items:
            price=item.product_varient.product.offer_price
   
            OrderItems.objects.create(order=order,product_varient=item.product_varient,price=price,quantity=item.quantity,payment_status='Paid')
            product_varient=item.product_varient
            product_varient.stock=product_varient.stock-item.quantity
            product_varient.save()
            
         cart_items=Cart.objects.filter(user=user)
         cart_items.delete()
         messages.success(request, 'order placed successfully')

         WalletTransaction.objects.create(user=user,wallet=wallet,amount=total_amount,transaction_type='Payment')

         Payment.objects.create(order=order,amount=total_amount,payment_method='Wallet')

         return render(request,'user_order/success.html',{'address':address,'order_items':order_items,'total_amount':total_amount,'payment_method':'Wallet'})
      else:
         messages.error(request, 'insuffisient balance in your wallet')
         return redirect('checkout_payment')
   except Exception as e:

      messages.error(request, f'Error placing order: {str(e)}')
      return redirect('checkout_payment') 
   


@login_required(login_url='signin')
def razorpay_check(request):
   user=request.user
   name=user.first_name
   email=user.email
   phone_no=user.phone_no
   total_amount=int((request.session['order_data']['total_amount'])*100)

   client = razorpay.Client(auth=(settings.KEY, settings.SECRET))

   key=settings.KEY     
   payment = client.order.create({
         'amount': total_amount,
         'currency': 'INR', 
         'payment_capture': 1
              
    })
   
   return JsonResponse({'total_amount':total_amount,'name':name,'email':email,'phone_no':phone_no,'key':key})



def online_payment(request):
   try:
      
      payment_id=request.POST['payment_id']

      user=request.user
      address_id=request.session.get('selected-address')
      selected_address=Address.objects.get(id=address_id)
      total_amount=request.session['order_data']['total_amount']
      order_items=Cart.objects.filter(user=user)

      name=selected_address.name
      order_address=selected_address.address
      phone_no=selected_address.phone_no
      pincode=selected_address.pincode
      city=selected_address.city
      state=selected_address.state
      alternative_phone_no=selected_address.alternative_phone_no

      address=OrderAddress.objects.create(name=name,address=order_address,phone_no=phone_no,pincode=pincode,
                                          city=city,state=state,alternative_phone_no=alternative_phone_no)
      
      order=Order.objects.create(user=user,address=address,payment_method='Online_Payment',total_amount=total_amount)
      for item in order_items:
         price=item.product_varient.product.offer_price
         OrderItems.objects.create(order=order,product_varient=item.product_varient,price=price,quantity=item.quantity,payment_status='Paid')
         product_varient=item.product_varient
         product_varient.stock=product_varient.stock-item.quantity
         product_varient.save()
      
      Payment.objects.create(order=order,amount=total_amount,payment_method='Razorpay',razorpay_payment_id=payment_id)
         
      cart_items=Cart.objects.filter(user=user)
      cart_items.delete()
      del request.session['selected-address']
      del request.session['cart_data']
      messages.success(request, 'order placed successfully')

      data = {'address':address,
              'order_items':order_items,
              'total_amount':total_amount,
              'payment_method':'RazorPay'}

      return render(request,'user_order/success.html',data)

   except Exception as e:
      messages.error(request, f'Error placing order: {str(e)}')
      return redirect('checkout_payment') 
      


@login_required(login_url='signin')
def order_list(request):
    if request.user.is_authenticated:
      user=request.user
      orders=Order.objects.filter(user=user).order_by('-id')
      order_items=[]
      for order in orders:
         order_items.extend(OrderItems.objects.filter(order=order).order_by('order__order_date'))
      
      items_per_page = 7
      paginator = Paginator(order_items, items_per_page)
      page = request.GET.get('page')

      try:
         order_items_paginated = paginator.page(page)
      except PageNotAnInteger:
         order_items_paginated = paginator.page(1)
      except EmptyPage:
         order_items_paginated = paginator.page(paginator.num_pages)

      return render(request, 'user_order/my-orders.html', {'order_items': order_items_paginated})
    else:
       return redirect('signin')


# def single_product_order(request,varient_id):

#    if 'product_data' in request.session:
#       product_varient=ProductVarient.objects.get(id=varient_id)
#       product_data=request.session.get('product_data')
#    else:
#       product_varient=ProductVarient.objects.get(id=varient_id)
#       quantity=1
#       price=product_varient.product.price
#       discount_price=product_varient.product.offer.first().discount_price
#       discount=price-discount_price
#       if discount_price>500:
#          delivery_charge=0
#       else:
#          delivery_charge=70
#       total_amount=discount_price+70   

#       data={
#          'varient_id':varient_id,
#          'product_price':price,
#          'discount':discount,
#          'delivery_charge':delivery_charge,
#          'total_amount':total_amount,
#          'quantity':quantity
#       }

#       request.session['product_data']=data
#       product_data=data
   

   

#    return render(request,'user_order/single-product-order.html',{'product_varient':product_varient,**product_data})

# def quantity_update(request):
#    quantity=int(request.GET.get('quantity'))
#    product_data=request.session.get('product_data')
#    product_data['quantity']=quantity
   

#    varient_id=product_data['varient_id']
#    product_varient=ProductVarient.objects.get(id=varient_id)
   
#    product_price=product_data['product_price']=product_varient.product.price * quantity
#    discount_price=product_varient.product.offer.first().discount_price*quantity
#    discount=product_data['discount']=product_price-discount_price
#    total_amount=product_data['total_amount']=product_price-discount
#    delivery_charge=product_data['delivery_charge']

#    request.session['product_data']=product_data

#    response={
#       'product_price':product_price,
#       'discount':discount,
#       'total_amount':total_amount,
#       'delivery_charge':delivery_charge
#    }

   
#    return JsonResponse(response)

@login_required(login_url='signin')
def cancel_order(request,orderitem_id):
   if request.user.is_authenticated:
      order_item=OrderItems.objects.get(id=orderitem_id)
      order_item.order_status='Canceled'
      quantity=order_item.quantity
      
      product=ProductVarient.objects.get(id=order_item.product_varient.pk)
      product.stock += quantity
      product.save()
      order_item.save()
      return redirect(request.META.get('HTTP_REFERER', '/'))
   return redirect('signin')


@login_required(login_url='signin')
def order_detail(request,orderitem_id):
   if request.user.is_authenticated:
      order_item=OrderItems.objects.get(id=orderitem_id)
      day=0
      if order_item.order_status == 'Delivered':
         day=(timezone.now()-order_item.delivery_date).days
      order=order_item.order
      return render(request,'user_order/order-details.html',{'order':order,'order_item':order_item,'day':day})
   else:
      return redirect('signin')
   

@login_required(login_url='signin')
def return_request(request,orderitem_id):
   item=OrderItems.objects.get(id=orderitem_id)
   if (timezone.now()-item.delivery_date).days < 14:
      item.return_status='Request'
      item.save()
      return redirect(request.META.get('HTTP_REFERER', '/'))
   else:
      messages.error(request, "Out of date")
      return redirect(request.META.get('HTTP_REFERER', '/'))




from django.template.loader import render_to_string
from xhtml2pdf import pisa

def invoice_pdf(request,orderitem_id):
    
    order_item= OrderItems.objects.get(id=orderitem_id)
    total_price=order_item.price*order_item.quantity

    context={
       'order_item':order_item,
       'total_price':total_price

    }

    template = 'user_order/invoice-pdf.html'
    html_string = render_to_string(template, context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="invoice.pdf"'

    pisa_status = pisa.CreatePDF(html_string, dest=response )
    
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html_string + '</pre>')
    return response







   
  
   

