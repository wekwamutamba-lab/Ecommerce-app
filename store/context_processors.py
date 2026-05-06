# store/context_processors.py

def cart_context(request):
    """
    Makes cart_count available in EVERY template automatically.
    This is how the navbar badge always shows the right number
    without you passing it manually from every single view.
    """
    cart       = request.session.get('cart', {})
    cart_count = sum(item['quantity'] for item in cart.values())
    return {'cart_count': cart_count}