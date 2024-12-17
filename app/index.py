from calendar import month
from datetime import datetime
from flask import render_template, request, jsonify ,url_for, redirect
from app import app, login
from app.utils import revenue
from flask_login import login_user,logout_user

@login.user_loader
def load_user(user_id):
    return utils.get_user_by_id(user_id)

@app.route("/") # Định tuyến khi người dùng truy cập vào trang chủ sẽ gọi hàm index()
def index():
    return render_template('index.html')

@app.route("/admin_stats")
def admin_view():
    month = request.args.get('month', datetime.now().month)
    year = request.args.get('year', datetime.now().year)
    return render_template('template_admin/index.html',
                           month_revenue_total=utils.month_revenue_total(month=month),
                           year_revenue_total=utils.year_revenue_total(year=year),
                           stats=utils.revenue(type_revenue='revenue-day', month=month, year=year))

@app.route("/admin_stats/login", methods=['get', 'post'])
def admin_login():
    err_msg = ""
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        u = utils.auth_user(username=username,password=password)
        if u:
            login_user(u)
            return redirect('/admin_stats')
        else:
            err_msg="Tai khoan hoac mat khau sai !!!"
    return render_template('template_admin/login.html',err_msg=err_msg)


@app.route("/admin_stats/register")
def register():
    return render_template('template_admin/register.html')


@app.route("/admin_stats/forgot-password")
def forgot_password():
    return render_template('template_admin/forgot-password.html')


@app.route("/admin_stats/table-revenue")
def table_revenue():
    month = request.args.get('month', datetime.now().month)
    year = request.args.get('year', datetime.now().year)
    type_revenue = request.args.get('type_revenue')

    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')

    return render_template('template_admin/table-revenue.html',
                           type_revenue=type_revenue,
                           stats=utils.revenue(type_revenue=type_revenue, month=month, year=year),
                           stats_book=utils.revenue_book(from_date=from_date, to_date=to_date))


@app.route("/admin_stats/table-inventory")
def table_inventory():
    return render_template('template_admin/table-inventory.html',  stats=utils.inventory_stats())


@app.route("/admin_stats/chart-inventory")
def chart_inventory():
    return render_template('template_admin/chart-inventory.html', inventory_stats=utils.inventory_stats())

@app.route("/admin_stats/chart-revenue")
def chart_revenue():
    month = request.args.get('month', datetime.now().month)
    year = request.args.get('year', datetime.now().year)
    type_revenue = request.args.get('type_revenue')

    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')

    return render_template('template_admin/chart-revenue.html',
                           type_revenue=type_revenue,
                           stats=utils.revenue(type_revenue=type_revenue, month=month, year=year),
                           stats_book=utils.revenue_book(from_date=from_date, to_date=to_date))

@app.route("/admin_stats/register", methods=['get','post'])
def admin_register():
    err_msg=""
    if request.method.__eq__('POST'):
        name=request.form.get('name')
        username=request.form.get('username')
        phone_number=request.form.get('phone_number')
        password=request.form.get('password')
        confirm=request.form.get('confirm')
        try:
            if password.strip().__eq__(confirm.strip()):
                utils.add_user(name=name,username=username,password=password,phone_number=phone_number)
                return redirect(url_for('index'))
            else:
                err_msg='MAT KHAU KHONG KHOP !!!'
        except Exception as ex:
            err_msg="He thong dang co loi: " + str(ex)
    return render_template('template_admin/register.html',err_msg=err_msg)

@app.route("/admin_stats/book")
def book_manager():
    return render_template('template_admin/book.html')

@app.route('/admin_stats/logout')
def admin_logout():
    logout_user()
    return redirect(url_for('/admin_stats/login'))

if __name__ == "__main__":
    from app.admin import *
    app.run(debug=True)