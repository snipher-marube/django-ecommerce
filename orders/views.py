from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import datetime
from .models import Order
from carts.models import CartItem
from .forms import OrderForm

@login_required
def place_order(request, total=0, quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()

    if cart_count <= 0:
        return redirect('products')

    tax = 0
    grand_total = 0
    shipping_fee = 0

    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity

    tax = (2 * total) / 100
    shipping_fee = (3 * total) / 100
    grand_total = total + tax + shipping_fee

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = current_user
            data.tax = tax
            data.shipping_fee = shipping_fee
            data.order_total = grand_total
            data.ip = request.META.get('REMOTE_ADDR')

            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime('%Y%m%d')
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            return redirect('order_success')  # Redirect to a success page
    else:
        form = OrderForm()

    context = {
        'form': form,
        'cart_items': cart_items,
        'grand_total': grand_total,
        'tax': tax,
        'shipping_fee': shipping_fee,
        'total': total,
    }
    return render(request, 'orders/checkout.html', context)


def success(request):
    return render(request, 'orders/success.html')
