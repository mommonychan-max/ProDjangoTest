console.log("TechNova loaded");

function confirmDelete(){
    return confirm("Are you sure you want to delete this?");
}

document.querySelectorAll('.add-cart-btn').forEach(button => {
    button.addEventListener('click', function () {
        const currentButton = this;

        fetch(this.dataset.url, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            credentials: 'same-origin',
        })
        .then(response => response.json())
        .then(data => {

            // Update cart badge  ✅ CHANGE THIS BLOCK
            let badge = document.querySelector('.cart-badge:not(.wishlist-badge)');
            if (badge) {
                badge.textContent = data.cart_count;
                badge.style.display = data.cart_count > 0 ? 'flex' : 'none';
                badge.style.alignItems = 'center';
                badge.style.justifyContent = 'center';
            }

            currentButton.innerHTML = 'Added ✓';
            setTimeout(() => {
                currentButton.innerHTML = 'Add to Cart';
            }, 1000);

        });
    });
});