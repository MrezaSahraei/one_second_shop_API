from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import Cart
from django.conf import settings
@receiver(user_logged_in) #when user logged in
def merge_carts_when_login(sender, request, user, **kwargs):
    session_key = request.COOKIES.get('sessionid')
    Cart.merge_guest_cart(user, session_key)