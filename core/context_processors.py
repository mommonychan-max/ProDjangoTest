from cart.models import CartItem
from wishlist.models import Wishlist


def cart_counter(request):
    if request.user.is_authenticated:
        count = CartItem.objects.filter(user=request.user).count()
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
    else:
        count = 0
        wishlist_count = 0

    return {
        'cart_count': count,
        'wishlist_count': wishlist_count,
    }


