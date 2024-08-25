from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
import datetime
import json
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string

from products.models import Product
from .models import Order, Payment, OrderProduct
from carts.models import CartItem
from .forms import OrderForm

def payments(request):
    body = json.loads(request.body)
    
    # Process the payment
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])
    payment = Payment(
        user=request.user,
        payment_id=body['transID'],
        payment_method=body['payment_method'],
        amount_paid=order.order_total,
        status=body['status'],
    )
    payment.save()

    # Continue with order finalization if payment is successful
    if payment.status == 'Completed':
        order.payment = payment
        order.is_ordered = True
        order.save()

        # move the cart items to order product table
        cart_items = CartItem.objects.filter(user=request.user)

        for item in cart_items:
            orderproduct = OrderProduct()
            orderproduct.order_id = order.id
            orderproduct.payment = payment
            orderproduct.user_id = request.user.id
            orderproduct.product_id = item.product_id
            orderproduct.quantity = item.quantity
            orderproduct.product_price = item.product.price
            orderproduct.ordered = True
            orderproduct.save()

            cart_item = CartItem.objects.get(id=item.id)
            product_variation = cart_item.variations.all()
            orderproduct = OrderProduct.objects.get(id=orderproduct.id)
            orderproduct.variation.set(product_variation)
            orderproduct.save()

            # reduce the quantity of sold items
            product = Product.objects.get(id=item.product_id)
            product.stock -= item.quantity
            product.save()

        # clear cart
        CartItem.objects.filter(user=request.user).delete()

        # send order received email to customer
        mail_subject = 'Thank you for your order!'
        message = render_to_string('orders/order_received_email.html', {
            'user': request.user,
            'order': order,
        })
        to_email = request.user.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()

    # send order number and transaction id back to sendData method via JsonResponse
    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }

    return JsonResponse(data)

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
            data.save()

            # Generate order number
            order_number = f"{datetime.date.today().strftime('%Y%m%d')}{get_random_string(8).upper()}"
            data.order_number = order_number
            data.save()

            return redirect('payments')  # Redirect to payment view
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
