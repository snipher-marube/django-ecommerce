from django.db import models
from django.contrib.auth.models import User

from products.models import Product, Variation

class Cart(models.Model):
    cart_id = models.CharField(max_length=255, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, null=True, blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    quantity = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return self.product.product_name

    def sub_total(self):
        return self.product.price * self.quantity
    
    def total_discount(self):
        return self.product.discount * self.quantity
    
    