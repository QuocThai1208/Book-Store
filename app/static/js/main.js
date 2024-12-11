const mySelect = document.getElementById("type-revenue");
const inputRevenueMonth =  document.getElementById("txtInputOption");
const btnClick = document.getElementById('view-stats');
//Xử lý button xem báo cáo
btnClick.addEventListener('click', function (e){
    e.preventDefault();
    const type = document.getElementById('type-revenue').value;
    const year = document.getElementById("txtInputOption").value;
    const valueBtnClick = btnClick.value;
    // Thêm trạng thái hiển thị vào URL
    const showInput = type === 'revenue-month' ? 'true' : 'false';

    const url = `/admin/statsview/${valueBtnClick}?type_revenue=${encodeURIComponent(type)}&year=${year}&show_input=${showInput}`;
// chuyển hướng đến đường dẫn url
    window.location.href = url;
})


mySelect.addEventListener('change', function(e){
        const SelectValue = document.getElementById('type-revenue').value;
        if (SelectValue === 'revenue-month') {
            inputRevenueMonth.style.display='inline';
            inputRevenueMonth.removeAttribute('disabled');
            inputRevenueMonth.focus();
        }
        else {
        inputRevenueMonth.style.display = 'none'; // Ẩn input
        inputRevenueMonth.setAttribute('disabled', 'true'); // Vô hiệu hóa input
        }
    })


// Khôi phục trạng thái khi trang được tải
window.onload = function () {
    const params = new URLSearchParams(window.location.search);


    // Lấy giá trị của <select> từ URL
    const selectedType = params.get('type_revenue');
    if (selectedType) {
        mySelect.value = selectedType; // Đặt lại giá trị của <select>
    }


    const showInput = params.get('show_input');
    if (showInput === 'true') {
        inputRevenueMonth.style.display = 'inline';
        inputRevenueMonth.removeAttribute('disabled');
    } else {
        inputRevenueMonth.style.display = 'none';
        inputRevenueMonth.setAttribute('disabled', 'true');
    }
};
