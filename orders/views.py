from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
import datetime
import json
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.contrib import messages

from products.models import Product
from .models import Order, Payment, OrderProduct
from carts.models import CartItem
from .forms import OrderForm

def calculate_order_totals(cart_items):
    total = sum(item.product.price * item.quantity for item in cart_items)
    tax = (2 * total) / 100
    shipping_fee = (3 * total) / 100
    grand_total = total + tax + shipping_fee
    return total, tax, shipping_fee, grand_total

def generate_order_number():
    return f"{datetime.date.today().strftime('%Y%m%d')}{get_random_string(8).upper()}"

@login_required
def place_order(request):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)

    if cart_items.count() <= 0:
        return redirect('products')

    total, tax, shipping_fee, grand_total = calculate_order_totals(cart_items)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order(
                user=current_user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                state=form.cleaned_data['state'],
                city=form.cleaned_data['city'],
                postal_code=form.cleaned_data['postal_code'],
                street_address=form.cleaned_data['street_address'],
                tax=tax,
                shipping_fee=shipping_fee,
                order_total=grand_total,
                ip=request.META.get('REMOTE_ADDR'),
            )
            data.save()

            order_number = generate_order_number()
            data.order_number = order_number
            data.save()

            order = get_object_or_404(Order, user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'shipping_fee': shipping_fee,
                'grand_total': grand_total,
            }
            return render(request, 'orders/payments.html', context)
    else:
        initial_data = {
            'first_name': current_user.first_name,
            'last_name': current_user.last_name,
            'email': current_user.email,
        }
        form = OrderForm(initial=initial_data)

    context = {
        'form': form,
        'cart_items': cart_items,
        'grand_total': grand_total,
        'tax': tax,
        'shipping_fee': shipping_fee,
        'total': total,
    }
    return render(request, 'orders/checkout.html', context)

@login_required
def payments(request):
    try:
        body = json.loads(request.body)
        order = get_object_or_404(Order, user=request.user, is_ordered=False, order_number=body.get('orderID'))

        payment = Payment(
            user=request.user,
            payment_id=body.get('transID'),
            payment_method=body.get('payment_method'),
            amount_paid=order.order_total,
            status=body.get('status'),
        )
        payment.save()

        if payment.status == 'Completed':
            order.payment = payment
            order.is_ordered = True
            order.save()

            cart_items = CartItem.objects.filter(user=request.user)

            for item in cart_items:
                orderproduct = OrderProduct(
                    order=order,
                    payment=payment,
                    user=request.user,
                    product=item.product,
                    quantity=item.quantity,
                    product_price=item.product.price,
                    ordered=True
                )
                orderproduct.save()

                product_variation = item.variations.all()
                orderproduct.variation.set(product_variation)
                orderproduct.save()

                product = Product.objects.get(id=item.product_id)
                product.stock -= item.quantity
                product.save()

            CartItem.objects.filter(user=request.user).delete()

            mail_subject = 'Thank you for your order!'
            message = render_to_string('orders/order_received_email.html', {
                'user': request.user,
                'order': order,
            })
            to_email = request.user.email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

        data = {
            'order_number': order.order_number,
            'transID': payment.payment_id,
        }
        return JsonResponse(data)

    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def success(request):
    return render(request, 'orders/success.html')
