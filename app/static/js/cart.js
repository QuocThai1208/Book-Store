function addToCard(id, name, unit_price, img) {
    fetch('/api/carts', {
        method: 'post',
        body: JSON.stringify({
            "id": id,
            "name": name,
            "price": unit_price,
            "img": img,
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {

        let items = document.getElementsByClassName("cart-counter");
        for (let item of items)
            item.innerText = data.total_quantity;
    });
}

function addToCartWithQuantity(id, name, unit_price, img) {

    const quantity = parseInt(document.getElementById("quantity").value)
    fetch('/api/cart-with-quantity', {
        method: 'post',
        body: JSON.stringify({
            "id": id,
            "name": name,
            "price": unit_price,
            "img": img,
            "quantity": quantity
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {

        let items = document.getElementsByClassName("cart-counter");
        for (let item of items)
            item.innerText = data.total_quantity;
    });
}

function updateCart(id, obj) {
    fetch('/api/update-cart', {
        method: 'put',
        body: JSON.stringify({
            "id": id,
            "quantity": parseInt(obj.value)
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        if (obj.value == 0) {
            let e = document.getElementById("book " + id)
            e.style.display = "none"
        }

        let items = document.getElementsByClassName("cart-counter");
        for (let item of items)
            item.innerText = data.total_quantity;

        let amount = document.getElementById("totalAmount");
        amount.innerText = data.total_amount;
    });
}

function deleteCart(id) {
    if (confirm("Bạn chắc chắn xóa sách ra khỏi giỏ không?") == true) {
        fetch('/api/delete-cart/' + id, {
            method: 'delete',
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(res => res.json()).then(data => {

            let items = document.getElementsByClassName("cart-counter");
            for (let item of items)
                item.innerText = data.total_quantity;

            let amount = document.getElementById("totalAmount");
            amount.innerText = data.total_amount;

            let e = document.getElementById("book " + id)
            e.style.display = "none"
        }).catch(err => console.error(err))
    }
}

function pay() {
    if (confirm("Bạn chắc chắn thanh toán không?") === true) {
        fetch('/cre-order', {
            method: "post"
        }).then(res => res.json()).then(data => {
            if (data.status === 200) {
                alert("Thanh toán thành công!");
                location.reload()
            }
        });
    }
}

function createOnlineOrder(customer_id, list_book) {
    let payment_id = document.getElementById('select_payment');
    const orderData = {
        payment_id: payment_id.value,
        customer_id: customer_id,
        list_book: list_book,
    };

    fetch('/create-online-order', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(orderData)
    })
    .then(response => response.json())
    .then(data => {
       alert(data.message);
    })
    .catch(error => {
        console.error('Error creating order:', error);
    });
}