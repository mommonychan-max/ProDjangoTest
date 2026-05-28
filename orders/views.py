from django.shortcuts import render, redirect, get_object_or_404
from cart.models import CartItem
from .models import Order, OrderItem


def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)

    total = 0
    for item in cart_items:
        total += item.subtotal()

    if request.method == 'POST':
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

        return redirect('payment', order_id=order.id)

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total': total
    })


def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'order_history.html', {
        'orders': orders
    })


def manage_orders(request):
    orders = Order.objects.all().order_by('-created_at')

    return render(request, 'manage_orders.html', {
        'orders': orders
    })


def update_order_status(request, id):
    order = get_object_or_404(Order, id=id)

    if request.method == 'POST':
        order.status = request.POST.get('status')
        order.save()

    return redirect('manage_orders')