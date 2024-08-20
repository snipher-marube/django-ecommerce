from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product
from .models import Cart, CartItem

def _cart_id(request):
    """
    Retrieve or create a unique cart ID for the user's session.

    :param request: The HTTP request object.
    :return: A unique cart ID.
    """
    if not request.session.session_key:
        request.session.save()
    return request.session.session_key

def add_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    current_user = request.user

    if current_user.is_authenticated:
        # For authenticated users, use CartItem associated with the user
        cart_item, created = CartItem.objects.get_or_create(
            product=product,
            user=current_user,
            defaults={'quantity': 1}
        )
    else:
        # For anonymous users, use Cart associated with the session
        cart, created = Cart.objects.get_or_create(
            cart_id=_cart_id(request)
        )
        cart_item, created = CartItem.objects.get_or_create(
            product=product,
            cart=cart,
            defaults={'quantity': 1}
        )

    if not created:
        # If item already exists, update the quantity
        cart_item.quantity += 1
        cart_item.save()
        messages.info(request, f'Updated {product.product_name} quantity to {cart_item.quantity}.')
    else:
        messages.success(request, f'Added {product.product_name} to your cart.')

    return redirect('cart')

def cart(request):
    # Retrieve cart items for authenticated users or session-based cart for anonymous users
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart_id = _cart_id(request)
        cart_items = CartItem.objects.filter(cart__cart_id=cart_id)

    return render(request, 'carts/checkout.html', {'cart_items': cart_items})


'''def checkout(request):
    return render(request,'carts/checkout.html')'''
