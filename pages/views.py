from django.shortcuts import render

from products.models import Product

def home(request):
    products = Product.objects.filter(available=True)
    
    for product in products:
        product.averageReview = product.average_review()
    
    context = {
        'products': products,
    }
    return render(request, 'pages/home.html', context)

def contact(request):
    return render(request, 'pages/contact.html')