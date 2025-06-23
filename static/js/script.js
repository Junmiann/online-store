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

// Modal
document.addEventListener('DOMContentLoaded', function () {
    const editButtons = document.querySelectorAll('.edit-btn');
    editButtons.forEach(button => {
      button.addEventListener('click', function () {
        document.getElementById('modalProductId').value = this.dataset.id;
        document.getElementById('modalName').value = this.dataset.name;
        document.getElementById('modalImage').value = this.dataset.image;
        document.getElementById('modalQuantity').value = this.dataset.quantity;
        document.getElementById('modalPrice').value = this.dataset.price;
        document.getElementById('modalSupplier').value = this.dataset.supplier;
      });
    });
  });