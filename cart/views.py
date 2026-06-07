from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
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

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': 'This product is out of stock.',
                'cart_count': CartItem.objects.filter(user=request.user).count()
            })

        return redirect(request.META.get('HTTP_REFERER', 'products'))

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product
    )

    if created:
        cart_item.quantity = 1
        cart_item.save()
        message = 'Product added to cart.'
        success = True
    else:
        if cart_item.quantity < product.stock:
            cart_item.quantity += 1
            cart_item.save()
            message = 'Product quantity updated.'
            success = True
        else:
            message = 'Not enough stock available.'
            success = False

    cart_count = CartItem.objects.filter(user=request.user).count()

    if success:
        messages.success(request, message)
    else:
        messages.error(request, message)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': success,
            'message': message,
            'cart_count': cart_count
        })

    return redirect(request.META.get('HTTP_REFERER', 'products'))


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
    item = get_object_or_404(
        CartItem,
        id=id,
        user=request.user
    )

    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))

        if quantity < 1:
            quantity = 1

        item.quantity = quantity
        item.save()

    return redirect('cart')