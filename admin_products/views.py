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
        products = Products.objects.filter(is_deleted=False)
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
def add_category(request):
    if request.user.is_admin:
        form = CategoryForm()
        category = Category.objects.all()
        if request.method == "POST":
            form = CategoryForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return JsonResponse({"redirect_url": reverse("add_category")})
            else:
                return JsonResponse({"error": "Form is not valid"})

        return render(
            request,
            "admin_products/category.html",
            {"form": form, "category": category},
        )
    else:
        return redirect("admin_login")


@login_required(login_url="admin_login")
def delete_category(request, dlid):
    if request.user.is_admin:
        category = Category.objects.get(id=dlid)
        category.delete()
        return redirect("add_category")
    else:
        return redirect("admin_login")


@login_required(login_url="admin_login")
def edit_category(request, eid):
    if request.user.is_admin:
        category = Category.objects.get(id=eid)
        form = CategoryForm(instance=category)
        if request.method == "POST":
            form = CategoryForm(request.POST, request.FILES, instance=category)
            if form.is_valid():
                form.save()
                return redirect("add_category")
        else:
            return render(request, "admin_products/category.html", {"form": form})
    else:
        return redirect("admin_login")


@login_required(login_url="admin_login")
def add_brand(request):
    if request.user.is_admin:
        form = BrandForm()
        brand = Brand.objects.all()
        if request.method == "POST":
            form = BrandForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return JsonResponse({"redirect_url": reverse("add_brand")})
            else:
                return JsonResponse({"error": "Form is not valid"})

        return render(
            request, "admin_products/brands.html", {"form": form, "brand": brand}
        )
    else:
        return redirect("admin_login")


@login_required(login_url="admin_login")
def delete_brand(request, bid):
    if request.user.is_admin:
        brand = Brand.objects.get(id=bid)
        brand.delete()
        return redirect("add_brand")
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
                return redirect("add_products")
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
                price=form.cleaned_data.get('price')
                if product.offer:
                    discount=product.offer.first().discount
                    product.offer_price=price-(price*discount)/100
                elif product.category.category_offer:
                    discount=product.category.category_offer.discount
                    product.offer_price=price-(price*discount)/100
                else:
                    product.offer_price=price
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

            print(images)
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

                return JsonResponse({"redirect_url": reverse("product_varient")})

        return render(request, "admin_products/product-varient.html", {"form": form})
    else:
        return redirect("admin_login")


@login_required(login_url="admin_login")
def offer_management(request):
    if request.user.is_admin:
        form = ProductOfferForm()
        offers = ProductOffer.objects.all()
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
def category_offer(request):
    if request.user.is_admin:
        form = CategoryOfferForm()
        offers = CategoryOffer.objects.all()
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
                return redirect("category_offer")

        return render(
            request,
            "admin_products/category-offer.html",
            {"form": form, "offers": offers},
        )
    else:
        return redirect("admin_login")


def offer_price(request, discount, cid=None, pid=None):
    if cid:
        category = Category.objects.get(id=cid)
        products = Products.objects.filter(category=category)
        for product in products:
            if not product.offer.filter(product=product).exists():
                print("Inside if condition")
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