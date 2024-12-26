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

function buyNow1() {
    const quantity = parseInt(document.getElementById("quantity").value)
    const id = parseInt(document.getElementById("id").value)
    if (confirm("Bạn chắc chắn thanh toán không?") === true) {
        fetch('/buy-now', {
            method: "post",
            // body: JSON.stringify({
            //     quantity: quantity,
            //     id: id
            // })
        }).then(res => res.json()).then(data => {
            if (data.status === 200) {
                alert('Thanh toán thành công!');
            } else if (data.status === 400) {
                alert("Lỗi:" + data.message)
            }
        })
    }
}

function buyNow(bookId) {
    // Lấy số lượng từ input
    const quantity = document.getElementById('quantity').value;

    if (confirm("Bạn muốn đặt hàng sách này ngay??") === true) {
        fetch(`/buy_now/${bookId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                quantity: parseInt(quantity), // Số lượng sách cần đặt
            }),
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.error) {
                    alert(`Error: ${data.error}`);
                } else {
                    alert(`Đặt sách thành công! Mã đơn hàng: ${data.order_id}`);
                    window.location.href = '/payment';
                }
            })
            .catch((error) => {
                console.error('Error:', error);
                alert('Đã xảy ra lỗi không mong muốn.');
            });
    }
}

