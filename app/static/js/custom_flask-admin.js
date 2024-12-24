const inputImages = document.getElementById('inputImages');
const btnSubmit = document.getElementById('btnSubmit');
const preview = document.getElementById('preview');
const formData = new FormData();

// preview image
inputImages.addEventListener('change', function (){
    preview.innerHTML = ""; // Xóa nội dung cũ
    const images = this.files;
    for (let i = 0; i < images.length; i++) {
      const img = document.createElement('img');
      img.src = URL.createObjectURL(images[i]);
      img.style.width = "100px";
      img.style.margin = "5px";
      preview.appendChild(img);
    }
})

btnSubmit.addEventListener('click', function(){
      const images = inputImages.files;
      for (let i = 0; i < images.length; i++) {
            formData.append("image", images[i])
     }
        // Gửi dữ liệu qua fetch
        fetch('/api/upload-images', {
        method: 'POST',
        body: formData, // Chuyển mảng thành chuỗi JSON
    })
    .then(response => response.json()) // Xử lý phản hồi từ server
    .then(data => {
        if(data['status'] === 200 ){
            console.log(data['data'])
        }
    })
    .catch(error => {
        displayErrorToaster(error) // Xử lý lỗi
    });
})
