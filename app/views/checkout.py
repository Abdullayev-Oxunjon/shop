from django.shortcuts import redirect, render
from app.form import OrderForm
from app.models import Cart


def checkout_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        cart = Cart.objects.filter(user=request.user).first()
        cart_items = cart.cartitem_set.all()

        total_sum = 0
        for cart_item in cart_items:
            total_sum += cart_item.product.price * cart_item.quantity

    except Cart.DoesNotExist:
        cart_items = []
        total_sum = 0
        cart = None

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Foydalanuvchi to'lov ma'lumotlarini saqlash va buyurtmalar bazasiga yozish mumkin
            order = form.save(commit=False)
            order.user = request.user
            order.total_amount = total_sum
            if total_sum != 0:
                order.save()

            for cart_item in cart_items:
                # Buyurtma ro'yxatidagi har bir mahsulot uchun OrderItem yaratish mumkin,
                # agar kerak bo'lsa CartItem obyektini ishlatib olasiz
                pass

            # To'lov tizimi integratsiyasini amalga oshiring

            # Savatni tozalash
            if cart:
                cart.delete()

            return redirect('product-checkout-page')  # Yoki boshqa bir sahifaga o'tkazing

    else:
        form = OrderForm()

    return render(request, 'app/shop_main/checkout_page.html',
                  {'form': form, 'cart_items': cart_items, 'total_sum': total_sum})