from cart.models import CartItem

def cart_counter(request):

    if request.user.is_authenticated:

        count = CartItem.objects.filter(
            user=request.user
        ).count()

    else:
        count = 0

    return {
        'cart_count': count
    }