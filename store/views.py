# store/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product, Category


# ── HOME ──────────────────────────────────────────────────────────
def home(request):
    featured_products = Product.objects.filter(is_featured=True, in_stock=True)[:4]
    return render(request, 'store/home.html', {
        'featured_products': featured_products,
    })


# ── PRODUCT LIST (with search + category filter) ───────────────────
def product_list(request):
    products   = Product.objects.filter(in_stock=True)
    categories = Category.objects.all()

    # Filter by category slug if provided in URL query string
    selected_category = request.GET.get('category', '')
    if selected_category:
        products = products.filter(category__slug=selected_category)

    # Search by product name or description
    search_query = request.GET.get('q', '')
    if search_query:
        products = products.filter(name__icontains=search_query)

    return render(request, 'store/product_list.html', {
        'products':          products,
        'categories':        categories,
        'selected_category': selected_category,
        'search_query':      search_query,
    })


# ── ADD TO CART ────────────────────────────────────────────────────
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart    = request.session.get('cart', {})
    key     = str(product_id)

    if key not in cart:
        cart[key] = {
            'name':     product.name,
            'price':    str(product.price),
            'quantity': 1,
            'image':    product.image_url,
        }
        messages.success(request, f'"{product.name}" added to your cart.')
    else:
        messages.info(request, f'"{product.name}" is already in your cart.')

    request.session['cart'] = cart
    return redirect(request.META.get('HTTP_REFERER', 'product_list'))


# ── UPDATE CART QUANTITY ───────────────────────────────────────────
def update_cart(request, product_id):
    cart   = request.session.get('cart', {})
    key    = str(product_id)
    action = request.POST.get('action')   # 'increase' or 'decrease'

    if key in cart:
        if action == 'increase':
            cart[key]['quantity'] += 1
        elif action == 'decrease':
            if cart[key]['quantity'] > 1:
                cart[key]['quantity'] -= 1
            else:
                cart.pop(key)   # Remove if quantity hits 0

    request.session['cart'] = cart
    return redirect('cart')


# ── REMOVE FROM CART ───────────────────────────────────────────────
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    messages.info(request, 'Item removed from cart.')
    return redirect('cart')


# ── CART PAGE ──────────────────────────────────────────────────────
def cart_view(request):
    cart       = request.session.get('cart', {})
    cart_items = []
    subtotal   = 0

    for product_id, item in cart.items():
        item_total = float(item['price']) * item['quantity']
        subtotal  += item_total
        cart_items.append({
            'id':         product_id,
            'name':       item['name'],
            'price':      float(item['price']),
            'quantity':   item['quantity'],
            'image':      item.get('image', ''),
            'item_total': round(item_total, 2),
        })

    shipping    = 0 if subtotal >= 50 else 5.99    # Free shipping over $50
    order_total = round(subtotal + shipping, 2)

    return render(request, 'store/cart.html', {
        'cart_items':  cart_items,
        'subtotal':    round(subtotal, 2),
        'shipping':    shipping,
        'order_total': order_total,
    })


# ── CHECKOUT ───────────────────────────────────────────────────────
def checkout(request):
    cart       = request.session.get('cart', {})
    cart_items = []
    subtotal   = 0

    # Build order summary for sidebar
    for product_id, item in cart.items():
        item_total = float(item['price']) * item['quantity']
        subtotal  += item_total
        cart_items.append({
            'name':       item['name'],
            'price':      float(item['price']),
            'quantity':   item['quantity'],
            'item_total': round(item_total, 2),
        })

    shipping    = 0 if subtotal >= 50 else 5.99
    order_total = round(subtotal + shipping, 2)

    if request.method == 'POST':
        name    = request.POST.get('name', '').strip()
        email   = request.POST.get('email', '').strip()
        address = request.POST.get('address', '').strip()

        if name and email and address:
            request.session['cart'] = {}   # Clear cart on success
            return render(request, 'store/success.html', {
                'name':        name,
                'email':       email,
                'order_total': order_total,
                'item_count':  sum(i['quantity'] for i in cart_items),
            })

    return render(request, 'store/checkout.html', {
        'cart_items':  cart_items,
        'subtotal':    round(subtotal, 2),
        'shipping':    shipping,
        'order_total': order_total,
    })