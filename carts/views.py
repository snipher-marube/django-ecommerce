from django.shortcuts import render

def cart(request):
    return render(request, 'carts/cart.html')

def checkout(request):
    return render(request,'carts/checkout.html')
