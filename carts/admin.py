from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1
    readonly_fields = ('product', 'quantity', 'sub_total')
    can_delete = False
    verbose_name_plural = 'Cart Items'

    def has_add_permission(self, request, obj=None):
        return False  # Disable adding new cart items from this inline

    def has_change_permission(self, request, obj=None):
        return False  # Disable changing cart items from this inline

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'date_added')
    search_fields = ('cart_id',)
    readonly_fields = ('date_added',)
    list_filter = ('date_added',)
    inlines = [CartItemInline]

    

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'cart', 'quantity', 'is_active', 'sub_total')
    list_filter = ('is_active', 'product')
    search_fields = ('product__name', 'cart__cart_id', 'user__username')
    readonly_fields = ('sub_total',)
    autocomplete_fields = ('product', 'user')

    def sub_total(self, obj):
        return obj.sub_total()
    sub_total.short_description = 'Subtotal'
