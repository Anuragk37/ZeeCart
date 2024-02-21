from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from .models import *
from admin_products.forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url="admin_login")
def products(request):
    if request.user.is_admin:
        products = Products.objects.filter(is_deleted=False).order_by('-id')
        paginator = Paginator(products, 10)  # Show 10 products per page

        page = request.GET.get("page")
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        images = ProductImage.objects.all()
        return render(
            request,
            "admin_products/products.html",
            {"products": products, "images": images},
        )
    else:
        return redirect("admin_login")

@login_required(login_url="admin_login")
def category(request):
    if request.user.is_admin:
        category = Category.objects.filter(is_deleted=False).order_by('-id')

        return render(
            request,
            "admin_products/category.html",
            { "category": category},
        )
    else:
        return redirect("admin_login")
    
@login_required(login_url="admin_login")
def unlisted_category(request):
    if request.user.is_admin:
        category = Category.objects.filter(is_deleted=True)

        return render(
            request,
            "admin_products/unlisted-category.html",
            { "categories": category},
        )
    else:
        return redirect("admin_login")

@login_required(login_url="admin_login")
def add_category(request):
    if request.user.is_admin:
        form = CategoryForm()
        if request.method == "POST":
            form = CategoryForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return JsonResponse({"redirect_url": reverse("category")})
            else:
                return JsonResponse({"error": "Form is not valid"})

        return render(
            request,
            "admin_products/add-category.html",
            {"form": form},
        )
    else:
        return redirect("admin_login")


@login_required(login_url="admin_login")
def delete_category(request, dlid):
    if request.user.is_admin:
        category = Category.objects.get(id=dlid)
        category.is_deleted=True
        category.save()
        return redirect("category")
    else:
        return redirect("admin_login")

@login_required(login_url="admin_login")
def list_category(request, cid):
    if request.user.is_admin:
        category = Category.objects.get(id=cid)
        category.is_deleted=False
        category.save()
        return redirect("unlisted_category")
    else:
        return redirect("admin_login")


@login_required(login_url="admin_login")
def edit_category(request, eid):
    if request.user.is_admin:
        category = Category.objects.get(id=eid)

        if request.method == "POST":
            form = CategoryForm(request.POST, request.FILES, instance=category)
            if form.is_valid():
                form.save()
                return JsonResponse({"redirect_url": reverse("category")})
            else:
                return JsonResponse({"error": "Form is not valid"})
        else:
            form = CategoryForm(instance=category)
        
        return render(request, "admin_products/add-category.html", {"form": form})
    else:
        return redirect("admin_login")


@login_required(login_url="admin_login")
def brands(request):
    if request.user.is_admin:
        brand = Brand.objects.filter(is_deleted=False).order_by('-id')

        return render(
            request,
            "admin_products/brands.html",
            { "brand": brand},
        )
    else:
        return redirect("admin_login")

@login_required(login_url="admin_login")
def unlisted_brands(request):
    if request.user.is_admin:
        brands = Brand.objects.filter(is_deleted=True)

        return render(
            request,
            "admin_products/unlisted-brands.html",
            { "brands": brands},
        )
    else:
        return redirect("admin_login")


@login_required(login_url="admin_login")
def add_brand(request):
    if request.user.is_admin:
        form = BrandForm()
        if request.method == "POST":
            form = BrandForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return JsonResponse({"redirect_url": reverse("brands")})
            else:
                return JsonResponse({"error": "Form is not valid"})

        return render(
            request, "admin_products/add-brand.html", {"form": form}
        )
    else:
        return redirect("admin_login")


@login_required(login_url="admin_login")
def delete_brand(request, bid):
    if request.user.is_admin:
        brand = Brand.objects.get(id=bid)
        brand.is_deleted=True
        brand.save()
        return redirect("brands")
    else:
        return redirect("admin_login")

@login_required(login_url="admin_login")
def list_brand(request, bid):
    if request.user.is_admin:
        brand = Brand.objects.get(id=bid)
        brand.is_deleted=False
        brand.save()
        return redirect("unlisted_brands")
    else:
        return redirect("admin_login")

@login_required(login_url="admin_login")
def edit_brand(request, eid):
    if request.user.is_admin:
        brand = Brand.objects.get(id=eid)

        if request.method == "POST":
            form = BrandForm(request.POST, request.FILES, instance=brand)
            if form.is_valid():
                form.save()
                return JsonResponse({"redirect_url": reverse("brands")})
            else:
                return JsonResponse({"error": "Form is not valid"})
        else:
            form = BrandForm(instance=brand)
        
        return render(request, "admin_products/add-brand.html", {"form": form})
    else:
        return redirect("admin_login")

@login_required(login_url="admin_login")
def add_color(request):
    if request.user.is_admin:
        form = ColorForm()
        color = Color.objects.all()
        if request.method == "POST":
            form = ColorForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("add_color")
            else:
                return redirect("add_category")

        return render(
            request, "admin_products/color.html", {"form": form, "color": color}
        )
    else:
        return redirect("admin_login")


@login_required(login_url="admin_login")
def delete_color(request, dlid):
    if request.user.is_admin:
        color = Color.objects.get(id=dlid)
        color.delete()
        return redirect("add_color")
    else:
        return redirect("admin_login")


@login_required(login_url="admin_login")
def add_products(request):
    if request.user.is_admin:
        form = ProductForm()
        if request.method == "POST":
            form = ProductForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("product_varient")
        return render(request, "admin_products/add-products.html", {"form": form})
    else:
        return redirect("admin_login")


@login_required(login_url="admin_login")
def edit_product(request, eid):
    if request.user.is_admin:
        product = Products.objects.get(id=eid)
        form = ProductForm(instance=product)

        if request.method == "POST":
            form = ProductForm(request.POST, instance=product)
            if form.is_valid():
                price = form.cleaned_data.get('price')

                if product.offer.exists():
                    discount = product.offer.all().first().discount
                    product.offer_price = price - (price * discount) / 100
                elif product.category and product.category.category_offer:
                    discount = product.category.category_offer.first().discount
                    product.offer_price = price - (price * discount) / 100
                else:
                    product.offer_price = price

                product.save()
                form.save()

                return redirect("products")

        return render(request, "admin_products/add-products.html", {"form": form})
    else:
        return redirect("admin_login")


@login_required(login_url="admin_login")
def delete_product(request, dlid):
    if request.user.is_admin:
        product = Products.objects.get(id=dlid)
        product.is_deleted = True
        product.save()
        return redirect("products")
    else:
        return redirect("admin_login")


@login_required(login_url="admin_login")
def product_varient(request):
    if request.user.is_admin:
        form = ProductVarientForm()

        if request.method == "POST":
            form = ProductVarientForm(request.POST)
            images = request.FILES.getlist("images")

            images = [image for i, image in enumerate(images) if i >= len(images) / 2]
            if form.is_valid():
                product = form.cleaned_data.get("product")
                color = form.cleaned_data.get("color")
                new_stock = form.cleaned_data.get("stock")
                variant, created = ProductVarient.objects.get_or_create(
                    product=product, color=color, defaults={"stock": new_stock}
                )
                if not created:
                    variant.stock = models.F("stock") + new_stock
                    variant.save()

                for image in images:
                    ProductImage.objects.create(product_varient=variant, image=image)

                return JsonResponse({"redirect_url": reverse("products")})

        return render(request, "admin_products/product-varient.html", {"form": form})
    else:
        return redirect("admin_login")


@login_required(login_url="admin_login")
def offer_management(request):
    if request.user.is_admin:
        form = ProductOfferForm()
        offers = ProductOffer.objects.all().order_by('-id')
        if request.method == "POST":
            form = ProductOfferForm(request.POST)
            if form.is_valid():
                product = form.cleaned_data.get("product")
                new_discount = form.cleaned_data.get("discount")
                existing_offer = ProductOffer.objects.filter(product=product).first()
                if existing_offer:
                    existing_offer.discount = new_discount
                    existing_offer.save()
                else:
                    form.save()

                offer_price(request, new_discount, pid=product.id)

                return redirect("offer_management")

        return render(
            request, "admin_products/offers.html", {"form": form, "offers": offers}
        )
    else:
        return redirect("admin_login")

@login_required(login_url="admin_login")
def deactivate_product_offer(request,oid):
    if request.user.is_admin:
        offer=ProductOffer.objects.get(id=oid)
        offer.is_active=False
        offer.save()
        product=offer.product
        category=product.category
        category_offer_exist=CategoryOffer.objects.filter(category=category,is_active=True).exists()
        if not category_offer_exist:
            product.offer_price=product.price
            product.save()
        else:
            category_offer=CategoryOffer.objects.get(category=category,is_active=True)
            product.offer_price = product.price - (product.price * category_offer.discount) / 100
            product.save()
            
        return redirect('offer_management')
    else:
        return redirect("admin_login")


@login_required(login_url="admin_login")
def activate_product_offer(request,oid):
    if request.user.is_admin:
        offer=ProductOffer.objects.get(id=oid)
        offer.is_active=True
        offer.save()
        product=offer.product
        product.offer_price = product.price - (product.price * offer.discount) / 100
        product.save()
            
        return redirect('offer_management')
    else:
        return redirect("admin_login")



@login_required(login_url="admin_login")
def category_offer(request):
    if request.user.is_admin:
        form = CategoryOfferForm()
        offers = CategoryOffer.objects.all().order_by('-id')
        if request.method == "POST":
            form = CategoryOfferForm(request.POST)
            if form.is_valid():
                category = form.cleaned_data.get("category")
                new_discount = form.cleaned_data.get("discount")
                existing_offer = CategoryOffer.objects.filter(category=category).first()

                if existing_offer:
                    existing_offer.discount = new_discount
                    existing_offer.save()
                else:
                    form.save()
                offer_price(request, new_discount, cid=category.id)

                return redirect("category_offer")

        return render(
            request,
            "admin_products/category-offer.html",
            {"form": form, "offers": offers},
        )
    else:
        return redirect("admin_login")

@login_required(login_url="admin_login")
def deactivate_category_offer(request,oid):
    if request.user.is_admin:
        offer=CategoryOffer.objects.get(id=oid)
        offer.is_active=False
        offer.save()
        category=offer.category
        products=Products.objects.filter(category=category)
        for product in products:
                if not product.offer.filter(product=product,is_active=True).exists():
                    product.offer_price = product.price
                    product.save()
        return redirect('category_offer')
    else:
        return redirect("admin_login")

@login_required(login_url="admin_login")
def activate_category_offer(request,oid):
    if request.user.is_admin:
        offer=CategoryOffer.objects.get(id=oid)
        offer.is_active=True
        offer.save()
        category=offer.category
        products=Products.objects.filter(category=category)
        for product in products:
                if not product.offer.filter(product=product,is_active=True).exists():
                    product.offer_price = product.price - (product.price * offer.discount) / 100
                    product.save()
        return redirect('category_offer')
    else:
        return redirect("admin_login")


def offer_price(request, discount, cid=None, pid=None):
    if cid:
        category = Category.objects.get(id=cid)
        products = Products.objects.filter(category=category)
        for product in products:
            if not product.offer.filter(product=product).exists():
                product.offer_price = product.price - (product.price * discount) / 100
                product.save()
    if pid:
        product = Products.objects.get(id=pid)
        product.offer_price = product.price - (product.price * discount) / 100
        product.save()


@login_required(login_url="admin_login")
def deleted_products(request):
    if request.user.is_admin:
        products = Products.objects.filter(is_deleted=True)
        images = ProductImage.objects.all()
        return render(
            request,
            "admin_products/deleted-products.html",
            {"products": products, "images": images},
        )
    else:
        return redirect("admin_login")


@login_required(login_url="admin_login")
def restore_product(request, product_id):
    if request.user.is_admin:
        product = Products.objects.get(id=product_id)
        product.is_deleted = False
        product.save()
        return redirect("deleted_products")
    else:
        return redirect("admin_login")


# product view
@login_required(login_url="admin_login")
def product_view(request, product_id):
    if request.user.is_admin:
        product = Products.objects.get(id=product_id)
        return render(request, "admin_products/product-view.html", {"product": product})


@login_required(login_url="admin_login")
def delete_product_varient(request, varient_id):
    if request.user.is_admin:
        product_varient = ProductVarient.objects.get(id=varient_id)
        product_varient.delete()
        return redirect(request.META.get("HTTP_REFERER", "/"))


@login_required(login_url="admin_login")
def delete_image(request, image_id):
    if request.user.is_admin:
        image = ProductImage.objects.get(id=image_id)
        image.delete()
        return redirect(request.META.get("HTTP_REFERER", "/"))
