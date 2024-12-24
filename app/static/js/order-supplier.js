
const selectAllCheckbox = document.getElementById('selectAll');
const rowCheckboxes = document.querySelectorAll('.rowCheckBox');
const quantityInputs = document.querySelectorAll('.quantity-input');
const submitBtn = document.getElementById('submitBtn');
const exportPdf = document.getElementById('exportPdfBtn');
const divOrderSupplier = document.getElementById('order-supplier');
const btnBack = document.getElementById('backBtn');
const tbody = document.querySelector('#tableExportPdf tbody');
const dataOrder = [];

submitBtn.addEventListener('click', function(){
    rowCheckboxes.forEach((checkbox, index) => {
        if(checkbox.checked){
            dataOrder.push({
                employee_id:id,
                id:quantityInputs[index].id,
                quantity:quantityInputs[index].value
            });
        }
    })
        // Gửi dữ liệu qua fetch
        fetch('/api/submit-data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(dataOrder), // Chuyển mảng thành chuỗi JSON
    })
    .then(response => response.json()) // Xử lý phản hồi từ server
    .then(data => {
        if(data['status'] === 200 ){
            displaySuccessToaster()
            export_table(data['data'])
            divOrderSupplier.style.display = 'none'
            backBtn.classList.remove('d-none');
        }
    })
    .catch(error => {
        displayErrorToaster(error) // Xử lý lỗi
    });

})

//xuất file pdf
exportPdf.addEventListener('click', () => {
    const element = document.querySelector('.form-export'); // Chọn phần cần xuất PDF

    html2canvas(element).then(canvas => {
        const imgData = canvas.toDataURL('image/png'); // Chuyển thành hình ảnh PNG
        const pdf = new jspdf.jsPDF('p', 'mm', 'a4'); // Tạo PDF với khổ giấy A4

        const pdfWidth = pdf.internal.pageSize.getWidth(); // Chiều rộng     trang PDF
        const pdfHeight = (canvas.height * pdfWidth) / canvas.width; // Tính chiều cao giữ nguyên tỷ lệ

        pdf.addImage(imgData, 'PNG', 0, 10, pdfWidth, pdfHeight); // Thêm hình ảnh vào PDF
        pdf.save('chi-tiet-don-nhap-hang.pdf'); // Lưu file PDF
    });
});


function export_table(data){
    const dataBook = data['detail']
    const divName = document.getElementById('nameEmployee')
    const divDate = document.getElementById('createDate')
    const divId= document.getElementById('idOrderSupplier')

    divName.innerHTML = `Tên nhân viên: ${data.employeeName}`;
    divDate.innerHTML = `Thời gian tạo đơn: ${data.createDate}`;
    divId.innerHTML = `Mã đơn: ${data.orderId}`;

    dataBook.forEach(b => {
         const row = document.createElement('tr');
         row.innerHTML = `
            <td>${b.name}</td>
            <td>${b.quantity}</td>
            <td>${b.unitPrice}</td>
        `;
         tbody.appendChild(row);
    });
};

quantityInputs.forEach(input => {
        input.value = 150
        // Khi người dùng rời khỏi ô nhập
        input.addEventListener('blur', function () {
            if (this.value === '' || parseInt(this.value) < 150) {
                this.value = 150; // Đặt lại giá trị thành 150 nếu nhỏ hơn hoặc rỗng
            }
        });
})


rowCheckboxes.forEach((checkbox, index) => {
    checkbox.addEventListener('change', function() {
        quantityInputs[index].disabled = !this.checked;
    })
})

function displaySuccessToaster() {
    toastr.options.timeOut = 1500; // 1.5s
    toastr.success('Nhập sách thành công');
}

function displayErrorToaster(error) {
   toastr.options.timeOut = 1500; // 1.5s
   toastr.error(error);
}


// Hàm gán sự kiện cho các checkbox
function attachCheckboxListeners() {
    // Gán sự kiện thay đổi trạng thái cho từng checkbox
    rowCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateSelectAllState);
    });
}

// Hàm cập nhật trạng thái của checkbox "Select All"
function updateSelectAllState() {
    const isChecked = Array.from(rowCheckboxes).some(checkbox => checkbox.checked);//kiểm tra ít nhất 1 phần tử đc chọn
    submitBtn.disabled = !isChecked

    const allChecked = Array.from(rowCheckboxes).every(checkbox => checkbox.checked);//kiểm tra tất cả các phần tử được chọn
    selectAllCheckbox.checked = allChecked;
}

// Gán sự kiện cho checkbox "Select All"
selectAllCheckbox.addEventListener('change', function () {
    rowCheckboxes.forEach((checkbox, index) => {
        checkbox.checked = selectAllCheckbox.checked;
        quantityInputs[index].disabled = !selectAllCheckbox.checked;
        submitBtn.disabled = !selectAllCheckbox.checked;

    });
});


backBtn.addEventListener('click', function () {
    location.reload()
})

// Khởi tạo gán sự kiện khi tải trang
attachCheckboxListeners();

