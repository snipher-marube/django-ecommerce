from django.contrib import admin

from .models import Payment, Order, OrderProduct

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('payment', 'user', 'product', 'quantity', 'product_price', 'ordered')
    extra = 0
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'phone', 'email', 'city', 'order_total', 'status',  'is_ordered', 'created_at']
    list_filter = ['status', 'is_ordered', 'created_at']
    list_per_page = 20
    search_fields = ['order_number', 'first_name', 'last_name', 'phone', 'email']
    list_editable = ['status', 'is_ordered']

    inlines = [OrderProductInline]

    def full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'

    full_name.short_description = 'Name'
    
@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['user', 'order', 'payment', 'product', 'quantity', 'product_price', 'ordered']
    list_filter = ['ordered']
    list_per_page = 20
    search_fields = ['order__order_number', 'product__product_name']
    autocomplete_fields = ['user', 'product', 'order', 'payment']
    
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'payment_id', 'payment_method', 'amount_paid', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__first_name', 'payment_id']
    list_per_page = 20
