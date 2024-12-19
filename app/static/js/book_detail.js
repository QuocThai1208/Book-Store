function change_image(image) {

    var container = document.getElementById("main-image");

    container.src = image.src;
}


document.addEventListener("DOMContentLoaded", function (event) {


});

function decrementQuantity() {
    // Lấy phần tử input theo id
    const quantityInput = document.getElementById("quantity");
    // Chuyển giá trị hiện tại thành số nguyên
    let currentValue = parseInt(quantityInput.value, 10);
    // Giảm giá trị nếu lớn hơn 1
    if (currentValue > 1) {
        quantityInput.value = currentValue - 1;
    }
}

function incrementQuantity() {
    // Lấy phần tử input theo id
    const quantityInput = document.getElementById("quantity");
    // Chuyển giá trị hiện tại thành số nguyên
    let currentValue = parseInt(quantityInput.value, 10);
    // Tăng giá trị
    quantityInput.value = currentValue + 1;
}