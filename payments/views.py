from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from orders.models import Order
from .models import Payment


@login_required
def payment_view(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    existing_payment = Payment.objects.filter(order=order).first()

    if existing_payment:
        return redirect('receipt', order_id=order.id)

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

        messages.success(request, 'Payment successful.')

        return redirect('receipt', order_id=order.id)

    return render(request, 'payment.html', {
        'order': order
    })

@login_required
def receipt_view(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    payment = Payment.objects.filter(
        order=order
    ).first()

    return render(
        request,
        'receipt.html',
        {
            'order': order,
            'payment': payment
        }
    )

