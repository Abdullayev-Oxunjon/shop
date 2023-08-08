from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from app.models import Cart, CartItem, Product


@login_required(login_url='login')
def product_cart_page(request):
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        cart_items = cart.cartitem_set.all()
        cart_total = sum(item.total for item in cart_items)
    else:
        cart_items = []
        cart_total = 0
    return render(request=request,
                  template_name='app/shop_main/cart_page.html',
                  context={"cart_items": cart_items, "cart_total": cart_total})


@login_required(login_url='login')
def add_cart_view(request, product_id):
    product = Product.objects.filter(id=product_id).first()

    if request.method == "POST":
        quantity = int(request.POST['quantity'])
        cart = Cart.objects.create(user=request.user)
        if cart:
            cart = Cart.objects.filter(user=request.user).first()

        cart_items, created = CartItem.objects.get_or_create(product=product,
                                                             cart=cart)
        cart_items.quantity = cart_items.quantity - 1
        cart_items.quantity += quantity
        cart_items.save()
        return redirect('product-cart-page')
    else:
        cart = Cart.objects.create(user=request.user)
        if cart:
            cart = Cart.objects.filter(user=request.user).first()

        cart_items, created = CartItem.objects.get_or_create(product=product,
                                                             cart=cart)
        cart_items.quantity = 1
        cart_items.save()
        return redirect('product-cart-page')


@login_required(login_url='login')
def delete_cart_view(request, product_id):
    cart_item = CartItem.objects.filter(cart__user=request.user, id=product_id).first()
    if cart_item:
        cart_item.delete()
        return redirect('product-cart-page')


@login_required(login_url='login')
def edit_cart_item_view(request, product_id):

    try:
        cart_item = CartItem.objects.get(pk=product_id,
                                         cart__user=request.user)

        if request.method == 'POST':
            quantity = int(request.POST['quantity'])
            cart_item.quantity = quantity
            cart_item.save()

        return redirect('product-cart-page')

    except CartItem.DoesNotExist:
        pass

    return redirect('product-cart-page')
