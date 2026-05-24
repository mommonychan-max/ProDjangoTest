from django.shortcuts import render, redirect
from products.models import Product
from orders.models import Order
from django.contrib.auth.models import User


def dashboard_view(request):
    role = request.user.profile.role

    if role == 'admin':
        return redirect('admin_dashboard')

    elif role == 'staff':
        return redirect('admin_dashboard')

    else:
        return render(request, 'dashboard.html')


def admin_dashboard(request):
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_users = User.objects.count()
    recent_orders = Order.objects.all().order_by('-created_at')[:5]

    return render(request, 'admin_dashboard.html', {
        'total_products': total_products,
        'total_orders': total_orders,
        'total_users': total_users,
        'recent_orders': recent_orders
    })