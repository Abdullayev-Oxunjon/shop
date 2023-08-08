from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from app.models import Product, Wishlist


@login_required(login_url='login')
def product_wishlist_page(request):
    if request.user.is_authenticated:
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        products = wishlist.product.all()
        return render(request=request,
                      template_name='app/shop_main/wishlist_page.html',
                      context={"products":products})


@login_required(login_url='login')
def add_wishlist_view(request, product_id):
    product = get_object_or_404(klass=Product, id=product_id)

    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.product.add(product)
    return redirect("product-wishlist-page")


@login_required(login_url='login')
def delete_wishlist_view(request, product_id):
    product = get_object_or_404(klass=Product, id=product_id)

    wishlist = Wishlist.objects.get(user=request.user)
    wishlist.product.remove(product)
    return redirect('product-wishlist-page')

