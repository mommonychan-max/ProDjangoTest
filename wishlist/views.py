from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from products.models import Product
from .models import Wishlist


@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)

    return render(request, 'wishlist.html', {
        'wishlist_items': wishlist_items
    })


@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    if created:
        messages.success(request, 'Product added to wishlist.')
    else:
        messages.error(request, 'Product is already in wishlist.')

    return redirect('products')


@login_required
def remove_from_wishlist(request, id):
    wishlist_item = get_object_or_404(
        Wishlist,
        id=id,
        user=request.user
    )

    wishlist_item.delete()

    messages.success(request, 'Product removed from wishlist.')

    return redirect('wishlist')