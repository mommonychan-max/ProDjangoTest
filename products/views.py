from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator

from .models import Product, Category
from .forms import ProductForm, CategoryForm


def admin_or_staff_required(request):

    if request.user.profile.role not in ['admin', 'staff']:
        return False

    return True


def product_list(request):

    products = Product.objects.filter(is_active=True)

    categories = Category.objects.all()

    category_id = request.GET.get('category')

    search = request.GET.get('search')

    if category_id:
        products = products.filter(category_id=category_id)

    if search:
        products = products.filter(name__icontains=search)

    paginator = Paginator(products, 8)

    page_number = request.GET.get('page')

    products = paginator.get_page(page_number)

    return render(request, 'products.html', {
        'products': products,
        'categories': categories
    })


def product_detail(request, id):

    product = get_object_or_404(Product, id=id)

    return render(request, 'product_detail.html', {
        'product': product
    })


@login_required
def add_product(request):

    if not admin_or_staff_required(request):
        messages.error(request, 'You do not have permission.')
        return redirect('home')

    if request.method == 'POST':

        form = ProductForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Product added successfully.'
            )

            return redirect('manage_products')

    else:
        form = ProductForm()

    return render(request, 'add_product.html', {
        'form': form
    })


@login_required
def edit_product(request, id):

    if not admin_or_staff_required(request):
        messages.error(request, 'You do not have permission.')
        return redirect('home')

    product = get_object_or_404(Product, id=id)

    if request.method == 'POST':

        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Product updated successfully.'
            )

            return redirect('manage_products')

    else:
        form = ProductForm(instance=product)

    return render(request, 'edit_product.html', {
        'form': form,
        'product': product
    })


@login_required
def delete_product(request, id):

    if not admin_or_staff_required(request):
        messages.error(request, 'You do not have permission.')
        return redirect('home')

    product = get_object_or_404(Product, id=id)

    product.delete()

    messages.success(
        request,
        'Product deleted successfully.'
    )

    return redirect('manage_products')


@login_required
def manage_products(request):

    if not admin_or_staff_required(request):
        messages.error(request, 'You do not have permission.')
        return redirect('home')

    products = Product.objects.all().order_by('-created_at')

    return render(request, 'manage_products.html', {
        'products': products
    })