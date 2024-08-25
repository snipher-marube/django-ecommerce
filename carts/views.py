from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from products.models import Product, Variation
from .models import Cart, CartItem


def _cart_id(request):
    """
    Retrieve or create a unique cart ID for the user's session.

    :param request: The HTTP request object.
    :return: A unique cart ID.
    """
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    current_user = request.user # get the current user
    product = Product.objects.get(id=product_id) # get the product
    # if the user is authenticated
    if current_user.is_authenticated:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
            
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass
            
        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user)
            # existing variations -> database
            # current variation -> product_variation
            # item_id -> database
            # current item_id -> item_id
            existing_variation_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                existing_variation_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in existing_variation_list:
                # increase the cart item quantity
                index = existing_variation_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            else:
                # create a new cart item
                item = CartItem.objects.create(
                    product = product,
                    quantity = 1,
                    user = current_user,
                )
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()

        else:
        
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                user = current_user,
            )


            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()

        # show success message
        messages.success(request, "The product was successfully added to the cart")
        return redirect('cart')
    
    # if the user is not authenticated
    else:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
            
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass
            
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
            cart.save()
    
        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists() # check if the cartitem already exists
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart) # get the cartitem using the product and the cart
            # existing variations -> database
            # current variation -> product_variation
            # item_id -> database
            # current item_id -> item_id
            existing_variation_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                existing_variation_list.append(list(existing_variation))
                id.append(item.id)
        
            if product_variation in existing_variation_list:
                # increase the cart item quantity
                index = existing_variation_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
        
            else:
                # create a new cart item
                item = CartItem.objects.create(
                    product = product,
                    quantity = 1,
                    cart = cart,
                )
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()    
                
        else:
        
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
            )


            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        # show success message
        messages.success(request, "The product was successfully added to the cart")
        return redirect('cart')
    

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


