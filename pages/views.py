from django.shortcuts import render

from products.models import Product, Category

def home(request):
    products = Product.objects.filter(available=True)
    context = {
        'products': products
    }
    return render(request, 'pages/home.html', context)

def contact(request):
    return render(request, 'pages/contact.html')