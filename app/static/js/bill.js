
function addToBill(id, name, unit_price) {
    event.preventDefault()
    alert('Them vao don hang thanh cong !!!');
    fetch('/api/add-bill', {
        method: 'post',
        body: JSON.stringify({
            "id": id,
            "name": name,
            "price": unit_price
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        let items = document.getElementsById("bill-counter");
        for (let item of items)
            item.innerText = data.total_quantity;
    });
}
function updateBill(id, obj) {

    fetch('/api/update-bill', {
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
        console.log(data)

        let book_detail_quantity = document.getElementById('book-detail-quantity-' + id);
        book_detail_quantity.innerText = obj.value;

        let items = document.getElementsByClassName("bill-counter");
        for (let item of items)
            item.innerText = data.total_quantity;

        let amounts = document.getElementsByClassName("total-amount");
        for (let amount of amounts)
            amount.innerText = new Intl.NumberFormat().format(data.total_amount);
    });
}
function deleteBill(id, obj){
    if(confirm("Bạn có chắc chắn muốn xóa sản phẩm này không ?")==true) {
        fetch('/api/delete-bill/'+ id, {
        method: 'delete',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        if (obj.value == 0){
            let e = document.getElementById("book "+ id)
            e.style.display = "none"
        }
        console.log(data)
        let book_detail_quantity = document.getElementById('book-detail-' + id);
        book_detail_quantity.remove();

        let items = document.getElementsByClassName("bill-counter");
        for (let item of items)
            item.innerText = data.total_quantity;

        let amounts = document.getElementsByClassName("total-amount");
        for (let amount of amounts)
            amount.innerText = new Intl.NumberFormat().format(data.total_amount);

        let e=document.getElementById("book"+ id)
        e.style.display= "none"
    }).catch(err => console.error(err))
    }
}
function setDateToToday() {


   const p = document.getElementById('date_bill');
   const customer_name = document.getElementById('customer_name')
   const customer_name_detail = document.getElementById('customer_name_detail')

   const now = new Date();
   const year = now.getFullYear();
   const month = String(now.getMonth() + 1).padStart(2, '0');
   const day = String(now.getDate()).padStart(2, '0');
   const hours = String(now.getHours()).padStart(2, '0');
   const minutes = String(now.getMinutes()).padStart(2, '0');
   const formattedDateTime = `${day}-${month}-${year} ${hours}:${minutes}`;

   p.innerText = formattedDateTime;

    customer_name_detail.innerText = customer_name.value
}

function downloadPDF() {
    const { jsPDF } = window.jspdf;
    const pdf = new jsPDF();

    const element = document.querySelector('.modal-body');

    const elementHeight = element.scrollHeight * 2;
    const elementWidth = element.scrollWidth;

    html2canvas(element, {
        scale: 2,
        height: elementHeight,
        width: elementWidth
    }).then(canvas => {
        const imgData = canvas.toDataURL('image/png');

        const pdfWidth = pdf.internal.pageSize.getWidth();
        const pdfHeight = (canvas.height * pdfWidth) / canvas.width;

        pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);

        pdf.save('hoadon.pdf');
    }).catch(error => {
        console.error("Error generating PDF:", error);
    });
}


function createOrder(employee_id, list_book) {
    let guest_name = document.getElementById('customer_name');
    let payment_id = document.getElementById('select_payment');
    const orderData = {
        payment_id: payment_id.value,
        guest_name: guest_name.value,
        employee_id: employee_id,
        list_book: list_book,
    };

    fetch('/create-order', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(orderData)
    })
    .then(response => response.json())
    .then(data => {
    if(data.error){
        alert(data.error);
        window.location.href= '/employee/bill'
    }
    else{
       alert(data.message);
       downloadPDF();
       window.location.href= '/employee/bill'
    }
    })
    .catch(error => {
        console.error('Error creating order:', error);
    });
}

