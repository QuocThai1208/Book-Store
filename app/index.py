
from flask import render_template
from app import app



@app.route("/") # Định tuyến khi người dùng truy cập vào trang chủ sẽ gọi hàm index()
def index():
    return render_template('index.html')



if __name__ == "__main__":
    from app.admin import *
    app.run(debug=True)