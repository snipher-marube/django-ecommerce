from django.contrib import admin
from django.utils.html import format_html

import admin_thumbnails
from .models import Category, Product, ProductGallery, Variation, VariationCategory

class VariationInline(admin.TabularInline):
    model = Variation
    extra = 1  # Number of empty variations to show
    min_num = 1  # Minimum number of variations required
    max_num = 10  # Maximum number of variations allowed
    fields = ('variation_category', 'variation_value', 'is_active')
    autocomplete_fields = ['variation_category']
    show_change_link = True



@admin.register(VariationCategory)
class VariationCategoryAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'name', 'created')
    list_filter = ('created',)
    search_fields = ('name', 'display_name')
    ordering = ('-created',)
    prepopulated_fields = {'name': ('display_name',)}  # Automatically fills `name` based on `display_name`
    list_per_page = 20  # Paginate the list view
    save_on_top = True  # Save button is also on top
    fieldsets = (
        (None, {
            'fields': ('display_name', 'name')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('created',),
        }),
    )
    readonly_fields = ('created',)  # Ensure 'created' is not editable


@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active', 'created')
    list_filter = ('variation_category', 'is_active', 'created')
    search_fields = ('product__product_name', 'variation_value')
    list_editable = ('is_active',)
    ordering = ('-created',)
    autocomplete_fields = ['product', 'variation_category']
    list_per_page = 20
    save_as = True  # Save as new option in the change view

    fieldsets = (
        (None, {
            'fields': ('product', 'variation_category', 'variation_value', 'is_active')
        }),
        ('Metadata', {
            'classes': ('collapse',),
            'fields': ('created',),
        }),
    )
    readonly_fields = ('created',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('product', 'variation_category')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'slug')
    prepopulated_fields = {'slug': ('category_name',)}
    search_fields = ('category_name',)

@admin_thumbnails.thumbnail('image')
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
    
    inlines = [ProductGalleryInline, VariationInline]  # Variations are inline with Products
