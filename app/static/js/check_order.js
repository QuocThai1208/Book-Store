const btnDelete = document.getElementById('delete_order');
const id_orders = document.querySelectorAll("#order_id")
const data_Id_Order = [];
btnDelete.addEventListener('click', function () {
    id_orders.forEach(id => {
        data_Id_Order.push({id: id.innerText})
    })
    // Gửi dữ liệu qua fetch
        fetch('/api/data_Id_Order', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data_Id_Order), // Chuyển mảng thành chuỗi JSON
    })
    .then(response => response.json()) // Xử lý phản hồi từ server
    .then(data => {
        if(data['status'] === 200 ){
            location.reload()
            console.log(data['data'])
        }
    })
    .catch(error => {
        displayErrorToaster(error) // Xử lý lỗi
    });
})
