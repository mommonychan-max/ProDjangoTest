from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from cart.models import CartItem
from .models import Order, OrderItem


@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items.exists():
        messages.error(request, 'Your cart is empty.')
        return redirect('cart')

    total = 0
    for item in cart_items:
        total += item.subtotal()

    if request.method == 'POST':
        # Check stock before creating order
        for item in cart_items:
            if item.quantity > item.product.stock:
                messages.error(
                    request,
                    f'Not enough stock for {item.product.name}.'
                )
                return redirect('cart')

        order = Order.objects.create(
            user=request.user,
            full_name=request.POST.get('full_name'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            total_price=total,
            status='pending'
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

            item.product.stock -= item.quantity
            item.product.save()

        cart_items.delete()

        messages.success(request, 'Order created successfully.')

        return redirect('payment', order_id=order.id)

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total': total
    })


@login_required
def order_history(request):
    orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(request, 'order_history.html', {
        'orders': orders
    })


@login_required
def manage_orders(request):
    if request.user.profile.role not in ['admin', 'staff']:
        messages.error(request, 'You do not have permission.')
        return redirect('home')

    orders = Order.objects.all().order_by('-created_at')

    return render(request, 'manage_orders.html', {
        'orders': orders
    })


@login_required
def update_order_status(request, id):
    if request.user.profile.role not in ['admin', 'staff']:
        messages.error(request, 'You do not have permission.')
        return redirect('home')

    order = get_object_or_404(Order, id=id)

    if request.method == 'POST':
        order.status = request.POST.get('status')
        order.save()

        messages.success(request, 'Order status updated.')

    return redirect('manage_orders')