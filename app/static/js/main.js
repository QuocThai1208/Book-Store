const mySelect = document.getElementById("type-revenue");
const inputYear =  document.getElementById("inputYear");
const inputMonth =  document.getElementById("inputMonth");
const btnClick = document.getElementById('view-stats');
const divDate = document.querySelectorAll('.divDate');
//Xử lý button xem báo cáo
btnClick.addEventListener('click', function (e){
    e.preventDefault();
    const type = document.getElementById('type-revenue').value;
    const year = document.getElementById("inputYear").value;
    const month = document.getElementById("inputMonth").value;
    const from_date = document.getElementById("inputFromDate").value;
    const to_date = document.getElementById("inputToDate").value;

    const valueBtnClick = btnClick.value;

    let url = ``;
    if(type === 'revenue-book'){
        url = `/admin_stats/${valueBtnClick}?type_revenue=${encodeURIComponent(type)}&from_date=${from_date}&to_date=${to_date}`;
    }
    else if(type === 'revenue-month'){
        url = `/admin_stats/${valueBtnClick}?type_revenue=${encodeURIComponent(type)}&year=${year}`;
    }
    else if(type === 'revenue-day'){
        url = `/admin_stats/${valueBtnClick}?type_revenue=${encodeURIComponent(type)}&month=${month}&year=${year}`;
    }

// chuyển hướng đến đường dẫn url
    window.location.href = url;
})


mySelect.addEventListener('change', function(e){
        const SelectValue = document.getElementById('type-revenue').value;

        Show_Hide_Input(SelectValue);
    })


// Khôi phục trạng thái khi trang được tải
window.onload = function () {
    const params = new URLSearchParams(window.location.search);


    // Lấy giá trị của <select> từ URL
    const SelectValue = params.get('type_revenue');
    if (SelectValue) {
        mySelect.value = SelectValue; // Đặt lại giá trị của <select>
        Show_Hide_Input(SelectValue);
    }
};
function Show_Hide_Input(SelectValue){
         if (SelectValue === 'revenue-month') {

            divDate.forEach(div => {
                    div.style.display = 'none';
                })

            inputYear.style.display='inline';
            inputYear.removeAttribute('disabled');
            inputYear.focus();

            inputMonth.style.display = 'none'; // Ẩn input
            inputMonth.setAttribute('disabled', 'true');
        }
        else if(SelectValue === 'revenue-book'){

            divDate.forEach(div => {
                div.style.display = '';
            })

            inputYear.style.display = 'none'; // Ẩn input
            inputYear.setAttribute('disabled', 'true');

            inputMonth.style.display = 'none'; // Ẩn input
            inputMonth.setAttribute('disabled', 'true');
        }
        else if(SelectValue === 'revenue-day'){

            inputYear.style.display='inline';
            inputYear.removeAttribute('disabled');

            divDate.forEach(div => {
                div.style.display = 'none';
            })

            inputMonth.style.display='inline';
            inputMonth.removeAttribute('disabled');
            inputMonth.focus();
        }
}
