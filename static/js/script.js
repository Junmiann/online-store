let quantity = document.querySelector("#quantity");

const decrement = () => {
    if(quantity.value <= 1) {
        quantity.value = 1;
    } else {
        quantity.value = parseInt(quantity.value) - 1;
    }
}
const increment = () => {
    quantity.value = parseInt(quantity.value) + 1;
}