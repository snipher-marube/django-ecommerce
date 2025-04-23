from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.db import transaction

from products.models import Product, Variation
from .models import Cart, CartItem

def _get_cart_id(request):
    """Get or create a cart ID from the session."""
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key

def _get_cart_items(request):
    """Helper function to get cart items based on user authentication."""
    if request.user.is_authenticated:
        return CartItem.objects.filter(user=request.user, is_active=True)
    cart = Cart.objects.get(cart_id=_get_cart_id(request))
    return CartItem.objects.filter(cart=cart, is_active=True)

def _calculate_cart_totals(cart_items):
    """Calculate cart totals, taxes, and shipping."""
    total = sum(item.product.get_final_price() * item.quantity for item in cart_items)
    quantity = sum(item.quantity for item in cart_items)
    tax = round((2 * total) / 100, 2)
    shipping_fee = round((3 * total) / 100, 2)
    grand_total = round(total + tax + shipping_fee, 2)
    
    return {
        'total': total,
        'quantity': quantity,
        'tax': tax,
        'shipping_fee': shipping_fee,
        'grand_total': grand_total,
    }

@transaction.atomic
def add_cart(request, product_id):
    """Add a product to the cart with variations."""
    product = get_object_or_404(Product, id=product_id)
    product_variations = []
    
    if request.method == 'POST':
        for key, value in request.POST.items():
            try:
                variation = Variation.objects.get(
                    product=product,
                    variation_category__iexact=key,
                    variation_value__iexact=value,
                    is_active=True
                )
                product_variations.append(variation)
            except Variation.DoesNotExist:
                continue

    # Get or create cart item
    if request.user.is_authenticated:
        cart_item_filter = {'product': product, 'user': request.user}
    else:
        cart = Cart.objects.get_or_create(cart_id=_get_cart_id(request))[0]
        cart_item_filter = {'product': product, 'cart': cart}

    # Check for existing cart items with same variations
    cart_items = CartItem.objects.filter(**cart_item_filter)
    
    for item in cart_items:
        existing_variations = list(item.variations.all())
        if existing_variations == product_variations:
            if item.quantity < product.stock:  # Check stock before increasing
                item.quantity += 1
                item.save()
                messages.success(request, "Product quantity updated in cart")
            else:
                messages.warning(request, "Cannot add more than available stock")
            return redirect('cart')

    # Create new cart item if no matching variation exists
    if product.stock > 0:  # Only add if product is in stock
        cart_item = CartItem.objects.create(
            **cart_item_filter,
            quantity=1
        )
        if product_variations:
            cart_item.variations.add(*product_variations)
        messages.success(request, "Product added to cart successfully")
    else:
        messages.warning(request, "This product is currently out of stock")

    return redirect('cart')

@transaction.atomic
def remove_cart(request, product_id, cart_item_id):
    """Decrease product quantity in cart or remove if quantity is 1."""
    try:
        if request.user.is_authenticated:
            cart_item = get_object_or_404(
                CartItem, 
                product_id=product_id, 
                user=request.user, 
                id=cart_item_id
            )
        else:
            cart = get_object_or_404(Cart, cart_id=_get_cart_id(request))
            cart_item = get_object_or_404(
                CartItem, 
                product_id=product_id, 
                cart=cart, 
                id=cart_item_id
            )

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            messages.success(request, "Product quantity decreased")
        else:
            cart_item.delete()
            messages.success(request, "Product removed from cart")
            
    except Exception as e:
        messages.error(request, "Error updating cart")
        # Log the error here if you have logging setup

    return redirect('cart')

@transaction.atomic
def remove_cart_item(request, product_id, cart_item_id):
    """Completely remove a cart item."""
    try:
        if request.user.is_authenticated:
            cart_item = get_object_or_404(
                CartItem, 
                product_id=product_id, 
                user=request.user, 
                id=cart_item_id
            )
        else:
            cart = get_object_or_404(Cart, cart_id=_get_cart_id(request))
            cart_item = get_object_or_404(
                CartItem, 
                product_id=product_id, 
                cart=cart, 
                id=cart_item_id
            )
            
        cart_item.delete()
        messages.success(request, "Product removed from cart")
        
    except Exception as e:
        messages.error(request, "Error removing item from cart")
        # Log the error here

    return redirect('cart')

def cart(request):
    """Display the shopping cart with calculated totals."""
    context = {'cart_items': None}
    
    try:
        cart_items = _get_cart_items(request)
        totals = _calculate_cart_totals(cart_items)
        
        if request.method == 'POST':
            try:
                cart_item_id = request.POST.get('cart_item_id')
                new_quantity = int(request.POST.get('quantity', 1))
                product_id = request.POST.get('product_id')
                
                cart_item = get_object_or_404(CartItem, id=cart_item_id)
                product = get_object_or_404(Product, id=product_id)
                
                if new_quantity > product.stock:
                    messages.error(request, 'Quantity exceeds available stock')
                elif new_quantity < 1:
                    messages.error(request, 'Quantity must be at least 1')
                else:
                    cart_item.quantity = new_quantity
                    cart_item.save()
                    messages.success(request, 'Cart updated successfully')
                    return redirect('cart')
                    
            except (ValueError, ObjectDoesNotExist) as e:
                messages.error(request, 'Error updating cart quantity')
                # Log the error here

        context.update({
            'cart_items': cart_items,
            **totals
        })
        
    except ObjectDoesNotExist:
        messages.info(request, "Your cart is empty")
        
    return render(request, 'carts/cart.html', context)

@login_required
def checkout(request):
    """Display the checkout page with cart totals."""
    try:
        cart_items = _get_cart_items(request)
        if not cart_items.exists():
            messages.warning(request, "Your cart is empty")
            return redirect('cart')
            
        context = {
            'cart_items': cart_items,
            **_calculate_cart_totals(cart_items)
        }
        return render(request, 'carts/checkout.html', context)
        
    except ObjectDoesNotExist:
        messages.warning(request, "Your cart is empty")
        return redirect('cart')