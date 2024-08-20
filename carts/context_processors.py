from .models import Cart, CartItem
from .views import _cart_id

def counter(request):
    if 'admin' in request.path:
        return {}

    item_count = 0

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))

        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        item_count = sum(cart_item.quantity for cart_item in cart_items)
    except Cart.DoesNotExist:
        pass

    return {'item_count': item_count}
