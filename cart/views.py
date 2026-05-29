from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from products.models import Product
from .models import CartItem


@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)

    total = 0
    for item in cart_items:
        total += item.subtotal()

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if product.stock <= 0:
        messages.error(request, 'This product is out of stock.')
        return redirect('products')

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        if cart_item.quantity < product.stock:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, 'Product quantity updated.')
        else:
            messages.error(request, 'Not enough stock available.')
    else:
        messages.success(request, 'Product added to cart.')

    return redirect('cart')


@login_required
def remove_from_cart(request, id):
    cart_item = get_object_or_404(
        CartItem,
        id=id,
        user=request.user
    )

    cart_item.delete()

    messages.success(request, 'Product removed from cart.')

    return redirect('cart')


@login_required
def update_cart(request, id):
    cart_item = get_object_or_404(
        CartItem,
        id=id,
        user=request.user
    )

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))

        if quantity < 1:
            quantity = 1

        if quantity > cart_item.product.stock:
            quantity = cart_item.product.stock
            messages.error(request, 'Quantity changed to available stock only.')
        else:
            messages.success(request, 'Cart updated successfully.')

        cart_item.quantity = quantity
        cart_item.save()

    return redirect('cart')