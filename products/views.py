from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from carts.views import _cart_id
from carts.models import CartItem

from .models import Product, ProductGallery, Category, ReviewRating, VariationCategory, Variation
from orders.models import OrderProduct

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
    try:
        product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)

        # Check if the product is in the user's cart
        cart_id = _cart_id(request)
        in_cart = CartItem.objects.filter(cart__cart_id=cart_id, product=product).exists()
    except Exception as e:
        raise e
    
    # Fetch the product's gallery images
    gallery = ProductGallery.objects.filter(product=product)
    
    # Get reviews
    reviews = ReviewRating.objects.filter(product_id=product.id, status=True)
    
    # Get variations and categories
    variation_categories = VariationCategory.objects.filter(variations__product=product).distinct()
    variations = Variation.objects.filter(product=product, is_active=True)
    
    # Calculate the number of full and empty stars
    full_stars = range(int(product.average_review()))
    empty_stars = range(5 - int(product.average_review()))

    # Prepare the context for the template
    context = {
        'product': product,
        'gallery': gallery,
        'in_cart': in_cart,
        'reviews': reviews,
        'full_stars': full_stars,
        'empty_stars': empty_stars,
        'variation_categories': variation_categories,
        'variations': variations
    }

    return render(request, 'products/product_detail.html', context)
