from django.shortcuts import render, get_object_or_404

from .models import Product, ProductGallery

def products(request):
    products = Product.objects.filter(available=True)
    context = {
        'products': products
    }
    return render(request, 'products/products.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)
    except Exception as e:
        raise e
    
    # Get product Gallery
    gallery = ProductGallery.objects.filter(product_id=product)
    
    context = {
        'product': product,
        'gallery': gallery
    }
    
    return render(request, 'products/product_detail.html', context)
