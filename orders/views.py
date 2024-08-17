from django.shortcuts import render

def payment(request):
    return render(request, 'orders/payment.html')
