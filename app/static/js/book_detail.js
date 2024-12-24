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

// function createOrder(bookId, bookName, unitPrice, customerId) {
//     const quantity = document.getElementById('quantity').value;
//
//     // Dữ liệu gửi đến API
//     const orderData = {
//         customer_id: 2,
//         book_id: bookId,
//         quantity: parseInt(quantity),
//         unit_price: unitPrice
//     };
//
//     // Gọi API tạo đơn hàng
//     fetch('/api/orders', {
//         method: 'POST',
//         body: JSON.stringify(orderData)
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.error) {
//             alert(`Lỗi: ${data.error}`);
//         } else {
//             alert(`Đặt hàng thành công! Mã đơn hàng: ${data.order_id}`);
//             // Redirect hoặc cập nhật giao diện
//         }
//     })
//     .catch(error => {
//         console.error('Error:', error);
//         alert('Có lỗi xảy ra khi đặt hàng.');
//     });
// }
//
