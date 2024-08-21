from .models import Cart, CartItem
from .views import _cart_id

def counter(request):
    if 'admin' in request.path:
        return {}

    item_count = 0

    try:
        if request.user.is_authenticated:
            # Use CartItem to get the cart associated with the user
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        item_count = sum(cart_item.quantity for cart_item in cart_items)
    except Cart.DoesNotExist:
        pass

    return {'item_count': item_count}
