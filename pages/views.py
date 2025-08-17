from django.shortcuts import render

from products.models import Product, Category
from django.core.paginator import Paginator

def home(request):
    product_list = Product.objects.filter(available=True)
    paginator = Paginator(product_list, 12)  # Show 12 products per page
    page = request.GET.get('page')
    products = paginator.get_page(page)
    
    context = {
        'products': products,
    }
    return render(request, 'pages/home.html', context)

def contact(request):
    return render(request, 'pages/contact.html')