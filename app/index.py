from datetime import datetime
from flask import render_template, request
from app import app
from app.utils import revenue


@app.route("/") # Định tuyến khi người dùng truy cập vào trang chủ sẽ gọi hàm index()
def index():
    return render_template('index.html')


@app.route("/admin/statsview/login")
def login():
    return render_template('template_admin/login.html')


@app.route("/admin/statsview/register")
def register():
    return render_template('template_admin/register.html')


@app.route("/admin/statsview/forgot-password")
def forgot_password():
    return render_template('template_admin/forgot-password.html')


@app.route("/admin/statsview/table-revenue")
def table_revenue():
    year = request.args.get('year', datetime.now().year)
    type_revenue = request.args.get('type_revenue')
    return render_template('template_admin/table-revenue.html', type_revenue=type_revenue, stats=utils.revenue(type_revenue=type_revenue, year=year))


@app.route("/admin/statsview/table-inventory")
def table_inventory():
    return render_template('template_admin/table-inventory.html',  stats=utils.inventory_stats())


@app.route("/admin/statsview/chart-inventory")
def chart_inventory():
    return render_template('template_admin/chart-inventory.html', inventory_stats=utils.inventory_stats())

@app.route("/admin/statsview/chart-revenue")
def chart_revenue():
    year = request.args.get('year', datetime.now().year)
    type_revenue = request.args.get('type_revenue')
    return render_template('template_admin/chart-revenue.html', type_revenue=type_revenue, stats=utils.revenue(type_revenue=type_revenue, year=year))


if __name__ == "__main__":
    from app.admin import *
    app.run(debug=True)