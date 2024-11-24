
from flask import render_template
from app import app



@app.route("/") # Định tuyến khi người dùng truy cập vào trang chủ sẽ gọi hàm index()
def index():
    return render_template('report.html')


if __name__ == "__main__":
    app.run(debug=True)