def cart_context(request):
    cart = request.session.get('cart', {})
    cart_items = []
    cart_count = 0
    cart_total = 0

    for item in cart.values():
        item['subtotal'] = item['price'] * item['quantity']
        cart_items.append(item)
        cart_count += item['quantity']
        cart_total += item['subtotal']

    return {
        'cart_items': cart_items,
        'cart_count': cart_count,
        'cart_total': cart_total,
    }