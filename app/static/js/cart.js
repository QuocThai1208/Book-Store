function addToCard(id, name, unit_price, img) {
    fetch('/api/carts', {
        method: 'post',
        body: JSON.stringify({
            "id": id,
            "name": name,
            "price": unit_price,
            "img": img
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
        if (obj.value == 0){
            let e = document.getElementById("book "+ id)
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

            let e = document.getElementById("book "+ id)
            e.style.display = "none"
        }).catch(err => console.error(err))
    }
}