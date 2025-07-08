// Quantity (product page)
document.addEventListener("DOMContentLoaded", function() {
    const quantity = document.querySelector("#quantity");

    window.decrement = function() {
        if(quantity.value <= 1) {
            quantity.value = 1;
        } else {
            quantity.value = parseInt(quantity.value) - 1;
        }
    }

    window.increment = function() {
        if(quantity.value >= 10) {
            quantity.value = 10;
        } else {
            quantity.value = parseInt(quantity.value) + 1;
        }
    }
});

// Flash message
setTimeout(function(){
    var msg = document.getElementById("flash-msg");
    if (msg) {
        msg.style.display = "none";
    }
}, 3000);

// Product modal (admin page)
document.addEventListener('DOMContentLoaded', function () {
    const editButtons = document.querySelectorAll('.edit-btn');
    const form = document.querySelector('#productModal form');
    const deleteBtn = document.getElementById('deleteProductBtn');

    /* Add new product */
    const addButton = document.getElementById('addNewProductBtn');
    addButton.addEventListener('click', function () {
        form.action = this.dataset.action;

        document.getElementById('modalProductId').value = '';
        document.getElementById('modalName').value = '';
        document.getElementById('modalDescription').value = '';
        document.getElementById('modalImage').value = '';
        document.getElementById('modalQuantity').value = '';
        document.getElementById('modalPrice').value = '';
        document.getElementById('modalSupplierId').value = '';

        deleteBtn.style.display = 'none';
    });

    /* Edit */
    editButtons.forEach(button => {
        button.addEventListener('click', function () {
            form.action = this.dataset.action;

            document.getElementById('modalProductId').value = this.dataset.id;
            document.getElementById('modalName').value = this.dataset.name;
            document.getElementById('modalDescription').value = this.dataset.description;
            document.getElementById('modalImage').value = this.dataset.image;
            document.getElementById('modalQuantity').value = this.dataset.quantity;
            document.getElementById('modalPrice').value = this.dataset.price;
            document.getElementById('modalSupplierId').value = this.dataset.supplierId;

            deleteBtn.style.display = 'inline-block';
        });
    });

    /* Delete button */
    deleteBtn.addEventListener('click', function () {
        if (confirm("Are you sure you want to delete the product?")) {
            const productId = document.getElementById('modalProductId').value;
            const formDelete = document.createElement('form');
            formDelete.method = 'POST';
            formDelete.action = `/delete_product/${productId}`;
            document.body.appendChild(formDelete);
            formDelete.submit();
        }
    });
});