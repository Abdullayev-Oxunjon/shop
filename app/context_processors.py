from app.models import Cart


def items_in_cart(request):
    cart_items = None  # Boshlang'ich qiymatni beramiz
    cart_items_number = None
    cart_total = None

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart_items = cart.cartitem_set.all()
            cart_items_number = cart.cartitem_set.count()
            cart_total = sum(item.total for item in cart_items)

    return {
        'cart_items_nav': cart_items,
        'cart_items_nav_number': cart_items_number,
        'cart_items_total_nav': cart_total
    }