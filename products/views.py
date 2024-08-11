from django.shortcuts import render

def products(request):
    return render(request, 'products/products.html')

def product_detail(request):
    return render(request, 'products/product_detail.html')
