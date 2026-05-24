from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from .models import CartItem


def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)

    total = 0
    for item in cart_items:
        total += item.subtotal()

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


def remove_from_cart(request, id):
    cart_item = get_object_or_404(CartItem, id=id, user=request.user)
    cart_item.delete()
    return redirect('cart')


def update_cart(request, id):
    cart_item = get_object_or_404(CartItem, id=id, user=request.user)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        cart_item.quantity = quantity
        cart_item.save()

    return redirect('cart')