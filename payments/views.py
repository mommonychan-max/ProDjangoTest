from django.shortcuts import render, redirect, get_object_or_404
from orders.models import Order
from .models import Payment


def payment_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')

        Payment.objects.create(
            order=order,
            payment_method=payment_method,
            amount=order.total_price,
            status='paid'
        )

        order.status = 'processing'
        order.save()

        return redirect('order_history')

    return render(request, 'payment.html', {
        'order': order
    })