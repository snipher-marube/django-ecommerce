
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.urls import reverse

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

def is_safe_url(url, allowed_hosts):
    from urllib.parse import urlparse
    url = url.strip()
    if url == '':
        return False
    url_obj = urlparse(url)
    return url_obj.netloc in allowed_hosts

@login_required
def submit_review(request, product_id):
    # Get the product instance to retrieve the category_slug and product_slug
    product = get_object_or_404(Product, id=product_id)
    category_slug = product.category.slug
    product_slug = product.slug

    # Get the referer URL or fall back to the product detail page
    referer_url = request.META.get('HTTP_REFERER', reverse('product_detail', args=[category_slug, product_slug]))

    # Validate the referer URL to ensure it's safe
    if not is_safe_url(referer_url, allowed_hosts={request.get_host()}):
        referer_url = reverse('product_detail', args=[category_slug, product_slug])

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            # Update or create the review
            review, created = ReviewRating.objects.update_or_create(
                user=request.user,
                product_id=product_id,
                defaults={
                    'subject': form.cleaned_data['subject'],
                    'rating': form.cleaned_data['rating'],
                    'review': form.cleaned_data['review'],
                    'ip': request.META.get('REMOTE_ADDR'),
                }
            )
            if created:
                messages.success(request, 'Thank you! Your review has been submitted.')
            else:
                messages.success(request, 'Thank you! Your review has been updated.')
        else:
            messages.error(request, 'There was an error with your submission. Please correct the form.')
            return redirect(referer_url)

    # Redirect to the product detail page or the referer URL
    return redirect(referer_url)