from django.http import JsonResponse
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

    wishlist_item = Wishlist.objects.filter(user=request.user, product=product).first()

    if wishlist_item:
        # Already in wishlist → REMOVE it
        wishlist_item.delete()
        success = True
        message = 'Removed from wishlist.'
    else:
        # Not in wishlist → ADD it
        Wishlist.objects.create(user=request.user, product=product)
        success = True
        message = 'Added to wishlist.'

    wishlist_count = Wishlist.objects.filter(user=request.user).count()
    wishlist_product_ids = list(Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True))

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': success,
            'message': message,
            'wishlist_count': wishlist_count,
            'wishlist_product_ids': wishlist_product_ids,
            'product_id': product_id,
        })

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