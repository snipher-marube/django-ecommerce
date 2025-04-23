from allauth.account.adapter import DefaultAccountAdapter
from django.contrib import messages
from .views import _transfer_cart_to_user

class CartAccountAdapter(DefaultAccountAdapter):
    def login(self, request, user):
        super().login(request, user)
        transferred = _transfer_cart_to_user(request, user)
        if transferred:
            messages.info(request, f"Your {transferred} cart items have been transferred to your account")
    
    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit)
        if commit:
            transferred = _transfer_cart_to_user(request, user)
            if transferred:
                messages.info(request, f"Your {transferred} cart items have been transferred to your account")
        return user