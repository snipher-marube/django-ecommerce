from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product, Variation
from .models import Cart, CartItem


def _cart_id(request):
    """
    Retrieve or create a unique cart ID for the user's session.

    :param request: The HTTP request object.
    :return: A unique cart ID.
    """
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key

def add_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product_variation = []

    if request.method == 'POST':
        for key, value in request.POST.items():
            try:
                variation = Variation.objects.get(
                    product=product,
                    variation_category__iexact=key,
                    variation_value__iexact=value
                )
                product_variation.append(variation)
            except Variation.DoesNotExist:
                pass

    # Check if the user is authenticated
    if request.user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(
            product=product,
            user=request.user,
            defaults={'quantity': 1}
        )
    else:
        cart, created = Cart.objects.get_or_create(cart_id=_cart_id(request))
        cart_item, created = CartItem.objects.get_or_create(
            product=product,
            cart=cart,
            defaults={'quantity': 1}
        )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    if product_variation:
        cart_item.variations.set(product_variation)

    messages.success(request, "The product was successfully added to the cart")
    return redirect('cart')

def cart(request):
    return render(request, 'carts/checkout.html')


