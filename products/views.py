from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Product, ProductGallery, Category

def products(request, category_slug=None):
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category, available=True)[:12]
    else:
        products = Product.objects.filter(available=True).order_by('-created')

    paginator = Paginator(products, 18)  # Adjust items per page as needed
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If the page is not an integer, deliver the first page.
        products = paginator.page(1)
    except EmptyPage:
        # If the page is out of range, deliver the last page.
        products = paginator.page(paginator.num_pages)
    except Exception as e:
        # Handle any other unexpected exceptions
        products = paginator.page(1)  # fallback to the first page or handle as needed
        print(f"Pagination error: {e}")  # Log the error for debugging

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
