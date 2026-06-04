from django.shortcuts import render, redirect
from products.models import Product, Category
from .models import ContactMessage
from django.core.mail import send_mail
from django.conf import settings
from wishlist.models import Wishlist

def home(request):
    products = Product.objects.filter(is_active=True)[:8]
    categories = Category.objects.all()[:6]

    wishlist_product_ids = []
    if request.user.is_authenticated:
        wishlist_product_ids = list(Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True))

    return render(request, 'home.html', {
        'products': products,
        'categories': categories,
        'wishlist_product_ids': wishlist_product_ids,
    })


def about(request):
    return render(request, 'about.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        ContactMessage.objects.create(
            name=name,
            email=email,
            message=message
        )

        full_message = f"""
New message from FLUFFY website

Name: {name}
Email: {email}

Message:
{message}
"""

        send_mail(
            'New Contact Message',
            full_message,
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )

        return redirect('contact')

    return render(request, 'contact.html')
