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
            }
        })

        .then(response => response.json())

        .then(data => {

            const badge = document.querySelector('.cart-badge');

            if (badge) {
                badge.textContent = data.cart_count;
            }

            currentButton.innerHTML = 'Added ✓';

            setTimeout(() => {
                currentButton.innerHTML = 'Add to Cart';
            }, 1000);

        });

    });

});