from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Product, ProductGallery

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'slug')
    prepopulated_fields = {'slug': ('category_name',)}
    search_fields = ('category_name',)

class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="40" >'.format(object.image.url))
    
    list_display = ('thumbnail', 'product_name', 'slug', 'price', 'stock', 'available', 'created', 'updated')
    list_filter = ('available', 'created', 'updated')
    list_editable = ('price', 'stock', 'available')
    prepopulated_fields = {'slug': ('product_name',)}
    search_fields = ('product_name', 'description')
    date_hierarchy = 'created'
    ordering = ('-created',)
    list_display_links = ['product_name']
    
    inlines = [ProductGalleryInline]