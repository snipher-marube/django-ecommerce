from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Cart(models.Model):
    cart_id = models.CharField(max_length=255, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    quantity = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return self.product.product_name

    def sub_total(self):
        return self.product.price * self.quantity
