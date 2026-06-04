from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category
from .forms import ProductForm, CategoryForm


def product_list(request):
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all()

    category_id = request.GET.get('category')
    search = request.GET.get('search')

    if category_id:
        products = products.filter(category_id=category_id)

    if search:
        products = products.filter(name__icontains=search)

    return render(request, 'products.html', {
        'products': products,
        'categories': categories
    })


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_detail.html', {
        'product': product
    })


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('manage_products')
    else:
        form = ProductForm()

    return render(request, 'add_product.html', {
        'form': form
    })


def edit_product(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()
            return redirect('manage_products')
    else:
        form = ProductForm(instance=product)

    return render(request, 'edit_product.html', {
        'form': form,
        'product': product
    })


def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()
    return redirect('manage_products')


def manage_products(request):
    products = Product.objects.all()
    return render(request, 'manage_products.html', {
        'products': products
    })