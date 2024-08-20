from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages

from products.models import Product
from .models import Cart, CartItem

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # Safely get the product or return a 404
    current_user = request.user
    cart_item = None

    if current_user.is_authenticated:
        # Get or create a cart item for the authenticated user
        cart_item, created = CartItem.objects.get_or_create(
            product=product,
            user=current_user,
            defaults={'quantity': 1}
        )
    else:
        # Get or create the cart and cart item for the anonymous user
        cart, _ = Cart.objects.get_or_create(cart_id=_cart_id(request))
        cart_item, created = CartItem.objects.get_or_create(
            product=product,
            cart=cart,
            defaults={'quantity': 1}
        )

    if not created:
        # If the item is already in the cart, increase the quantity
        cart_item.quantity += 1
        cart_item.save()
        messages.info(request, f'Updated {product.product_name} quantity to {cart_item.quantity}.')
    else:
        messages.success(request, f'Added {product.product_name} to your cart.')

    return redirect('cart')



def cart(request):
    return render(request, 'carts/checkout.html')

'''def checkout(request):
    return render(request,'carts/checkout.html')'''
