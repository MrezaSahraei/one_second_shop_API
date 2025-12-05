from .models import CartItems, Cart

def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(buyer=request.user)
        return cart, created
    else:
        session_key = request.session.session_key

        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_id=session_key, defaults={'buyer': None})

        return cart, created


