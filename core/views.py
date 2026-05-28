from django.shortcuts import render, redirect
from products.models import Product, Category
from .models import ContactMessage


def home(request):
    products = Product.objects.filter(is_active=True)[:8]
    categories = Category.objects.all()[:6]

    return render(request, 'home.html', {
        'products': products,
        'categories': categories
    })


def about(request):
    return render(request, 'about.html')


def contact(request):
    if request.method == 'POST':
        ContactMessage.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            subject=request.POST.get('subject'),
            message=request.POST.get('message')
        )

        return redirect('contact')

    return render(request, 'contact.html')