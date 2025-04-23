from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from allauth.account.signals import user_signed_up, user_logged_in
from .views import _transfer_cart_to_user
from django.contrib import messages

User = get_user_model()

@receiver(user_signed_up)
def transfer_cart_on_signup(request, user, **kwargs):
    """
    Transfer cart items when a new user signs up.
    """
    transferred = _transfer_cart_to_user(request, user)
    if transferred:
        messages.info(request, f"Your {transferred} cart items have been transferred to your account")

@receiver(user_logged_in)
def transfer_cart_on_login(request, user, **kwargs):
    """
    Transfer cart items when an existing user logs in.
    """
    transferred = _transfer_cart_to_user(request, user)
    if transferred:
        messages.info(request, f"Your {transferred} cart items have been transferred to your account")