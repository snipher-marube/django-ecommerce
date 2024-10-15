from re import A
from urllib.parse import urlparse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .forms import ReviewForm
from carts.views import _cart_id
from carts.models import CartItem
from .models import Product, ProductGallery, Category, ReviewRating, VariationCategory, Variation

from django.conf import settings

ALLOWED_HOSTS = settings.ALLOWED_HOSTS


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
    
    # Calculate the review summary
    total_reviews = reviews.count()
    review_summary = {
        '5': reviews.filter(rating=5).count(),
        '4': reviews.filter(rating=4).count(),
        '3': reviews.filter(rating=3).count(),
        '2': reviews.filter(rating=2).count(),
        '1': reviews.filter(rating=1).count(),
    }
    if total_reviews > 0:
        for key in review_summary:
            review_summary[key] = (review_summary[key] / total_reviews) * 100
    else:
        for key in review_summary:
            review_summary[key] = 0

    # Prepare the context for the template
    context = {
        'product': product,
        'gallery': gallery,
        'in_cart': in_cart,
        'reviews': reviews,
        'full_stars': full_stars,
        'empty_stars': empty_stars,
        'variation_categories': variation_categories,
        'variations': variations,
        'review_summary': review_summary,
    }

    return render(request, 'products/product_detail.html', context)



def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)
            else:
                print(form.errors)
                return redirect(url)
