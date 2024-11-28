from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from products.models import Product, Variation
from .models import Cart, CartItem

def _cart_id(request):
    """
    Get or create a cart ID from the session.
    """
    if not request.session.session_key:
        request.session.create()

    cart_id = request.session.session_key
    return cart_id

def add_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product_variation = []

    # Extract variations from POST data
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

    # Determine cart ownership
    if request.user.is_authenticated:
        user = request.user
        cart = None
    else:
        cart_id = _cart_id(request)
        user = None
        cart, created = Cart.objects.get_or_create(cart_id=cart_id)

    # Check if the cart item already exists
    cart_items = CartItem.objects.filter(
        product=product,
        user=user,
        cart=cart
    )

    existing_variation_list = []
    id_list = []

    for item in cart_items:
        existing_variation = list(item.variations.all())
        existing_variation_list.append(existing_variation)
        id_list.append(item.id)

    if product_variation in existing_variation_list:
        # Increase the cart item quantity
        index = existing_variation_list.index(product_variation)
        item_id = id_list[index]
        item = CartItem.objects.get(id=item_id)
        item.quantity += 1
        item.save()
    else:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
            user=user
        )
        if product_variation:
            cart_item.variation.add(*product_variation)
            cart_item.save()

    messages.success(request, "The product has been added successfully to the cart")
    return redirect("cart")




def remove_cart(request, product_id, cart_item_id):
    
    product = get_object_or_404(Product, id=product_id) # get the product
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product_id, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id) # get the cartitem using the product and the cart
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    # show success message
    messages.success(request, "The product was successfully removed from the cart")
    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product_id, user=request.user, id=cart_item_id)
        cart_item.delete()
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
        product = get_object_or_404(Product, id=product_id) # get the product
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id) # get the cartitem using the product and the cart
        cart_item.delete()
    except:
        pass
    # show success message
    messages.success(request, "The product was successfully removed from the cart")
    return redirect('cart')

def cart(request, total=0, quantity=0, cart_items=None):
    try:
        shipping_fee = 0
        tax = 0
        grand_total = 0
        
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True) # get all the cart items using the cart
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        shipping_fee = (3 * total) / 100
        tax = (2 * total) / 100
        grand_total = total + tax + shipping_fee

        if request.method == 'POST':
            input_quantity = int(request.POST.get('quantity'))
            product_id = request.POST.get('product_id')
            product = Product.objects.get(id=product_id)

            if input_quantity > product.stock:
                messages.error(request, 'The quantity you entered is more than the available stock.')
            else:
                # Update the cart item quantity here
                cart_item = CartItem.objects.get(id=request.POST.get('cart_item_id'))
                cart_item.quantity = input_quantity
                cart_item.save()
                messages.success(request, 'Cart updated successfully.')

    except ObjectDoesNotExist:
        pass

    context = {
        'cart_items': cart_items,
        'total': total,
        'quantity': quantity,
        'tax': tax,
        'grand_total': grand_total,
        'shipping_fee': shipping_fee,
    }
    return render(request, 'carts/cart.html', context)

@login_required
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        shipping_fee = 0
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total) / 100
        shipping_fee = (3 * total) / 100
        grand_total = total + tax + shipping_fee

        
    except ObjectDoesNotExist:
        pass
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'quantity': quantity,
        'tax': tax,
        'grand_total': grand_total,
        'shipping_fee': shipping_fee,
    }
    return render(request, 'carts/checkout.html', context)


