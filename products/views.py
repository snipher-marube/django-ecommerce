from django.shortcuts import render, get_object_or_404
from .models import Product, ProductGallery, Category

def products(request, category_slug=None):
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category, available=True)
    else:
        products = Product.objects.filter(available=True).order_by('-created')
        
    context = {
        'products': products
    }
    return render(request, 'products/products.html', context)

def product_detail(request, category_slug, product_slug):
    product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)
    gallery = ProductGallery.objects.filter(product=product)
    
    context = {
        'product': product,
        'gallery': gallery
    }
    return render(request, 'products/product_detail.html', context)
