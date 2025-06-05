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
}, 4000);