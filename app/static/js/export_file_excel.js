// Hàm xử lý xuất dữ liệu từ bảng HTML sang Excel
document.getElementById("exportButton").addEventListener("click", function() {
    // Lấy bảng HTML
    const table = document.getElementById("dataTable");

    // Chuyển đổi bảng HTML thành dữ liệu Excel
    const wb = XLSX.utils.table_to_book(table, { sheet: "Sheet1" });

    // Xuất dữ liệu dưới dạng file Excel
    XLSX.writeFile(wb, "data_export.xlsx");
});
