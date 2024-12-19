import pdb
from calendar import month
from datetime import datetime
from flask import render_template, request, jsonify, session
from app import app
import math
from flask import render_template, request, jsonify, url_for, redirect
from flask import render_template, request, jsonify, url_for, redirect, Response
from sqlalchemy.ext.orderinglist import ordering_list

from app import app, login
from app.models import UserRole, Book, Order, TypeOrder
from app.utils import revenue
from flask_login import login_user, logout_user, current_user
import cv2
from pyzbar.pyzbar import decode


@login.user_loader
def load_user(user_id):
    return utils.get_user_by_id(user_id)


def admin_required(f):
    def wrap(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('admin_login'))
        if current_user.user_role != UserRole.ADMIN:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)

    wrap.__name__ = f.__name__
    return wrap

def employee_required(f):
    def wrap(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('employee_login'))
        if current_user.user_role != UserRole.EMPLOYEE:
            return redirect(url_for('employee_login'))
        return f(*args, **kwargs)

    wrap.__name__ = f.__name__
    return wrap

@app.route("/")  # Định tuyến khi người dùng truy cập vào trang chủ sẽ gọi hàm index()
def index():
    current_page = request.args.get("page", 1, type=int)
    cates = utils.load_categories()
    cate_id = request.args.get('category_id')
    kw = request.args.get('kw')
    page = request.args.get('page', 1)
    books = utils.load_books(cate_id=cate_id, kw=kw, page=int(page))

    page_size = app.config["PAGE_SIZE"]
    total = utils.count_books()
    return render_template('index.html', books=books, pages=math.ceil(total / page_size),
                           current_page=current_page)


@app.route("/books")
def books():
    current_page = request.args.get("page", 1, type=int)
    cates = utils.load_categories()
    cate_id = request.args.get('category_id')
    kw = request.args.get('kw')
    page = request.args.get('page', 1)
    books = utils.load_books(cate_id=cate_id, kw=kw, page=int(page))
    page_size = app.config["PAGE_SIZE"]
    total = utils.count_books(cate_id=cate_id, kw=kw)

    return render_template('list_books/books.html', books=books, pages=math.ceil(total / page_size),
                           current_page=current_page, kw=kw, category_id=cate_id)


@app.route("/books/<int:book_id>")
def book_detail(book_id):
    book = utils.get_book_by_id(book_id)
    image = utils.load_img_book(book_id)
    cates = utils.load_categories()

    return render_template('list_books/book_detail.html', book=book, image=image)


@app.route('/api/carts', methods=['post'])
def add_to_cart():
    cart = session.get('cart')
    if not cart:
        cart = {}

    id = str(request.json.get('id'))
    name = request.json.get('name')
    price = request.json.get('price')
    img = str(request.json.get('img'))

    if id in cart:
        cart[id]["quantity"] += 1
    else:
        cart[id] = {
            "id": id,
            "name": name,
            "price": price,
            'img': img,
            "quantity": 1
        }

    session['cart'] = cart

    return jsonify(utils.stats_cart(cart))


@app.route('/api/update-cart', methods=['put', 'delete'])
def update_cart():
    id = str(request.json.get('id'))
    quantity = request.json.get('quantity')

    cart = session.get('cart')

    if cart and id in cart:
        if int(quantity) == 0:
            del cart[id]
        else:
            cart[id]["quantity"] = int(quantity)

        session['cart'] = cart

    return jsonify(utils.stats_cart(cart))


@app.route('/api/delete-cart/<book_id>', methods=['delete'])
def delete_cart(book_id):
    cart = session.get('cart')

    if cart and book_id in cart:
        del cart[book_id]
        session['cart'] = cart

    return jsonify(utils.stats_cart(cart))


@app.route('/cart')
def cart():
    return render_template('cart.html')


@app.route("/admin_stats")
@admin_required
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
        user_role = request.form.get('user_role')
        u = utils.auth_user(username=username, password=password, role=UserRole.ADMIN)
        if u:
            login_user(u)
            return redirect('/admin_stats')
        else:
            err_msg = "Tai khoan hoac mat khau sai !!!"
    return render_template('template_admin/login.html', err_msg=err_msg)


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
    return render_template('template_admin/table-inventory.html', stats=utils.inventory_stats())


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


@app.route("/admin_stats/register", methods=['get', 'post'])
def admin_register():
    err_msg = ""
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        username = request.form.get('username')
        phone_number = request.form.get('phone_number')
        password = request.form.get('password')
        address = request.form.get('address')
        sex = request.form.get('sex')
        birth_day = request.form.get('birth_day')
        confirm = request.form.get('confirm')

        try:
            if password.strip().__eq__(confirm.strip()):
                utils.add_user(name=name, username=username,
                               password=password,
                               phone_number=phone_number,
                               user_role=UserRole.EMPLOYEE,
                               birth_day=birth_day,
                               address=address,
                               sex=sex
                               )
                return redirect('/employee/login')
            else:
                err_msg = 'MAT KHAU KHONG KHOP !!!'
        except Exception as ex:
            err_msg = "He thong dang co loi: " + str(ex)
    return render_template('template_admin/register.html', err_msg=err_msg)


@app.route("/customer/register", methods=['get', 'post'])
def customer_register():
    err_msg = ""
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        username = request.form.get('username')
        phone_number = request.form.get('phone_number')
        password = request.form.get('password')
        address = request.form.get('address')
        sex = request.form.get('sex')
        birth_day = request.form.get('birth_day')
        confirm = request.form.get('confirm')

        try:
            if password.strip().__eq__(confirm.strip()):
                utils.add_customer(name=name, username=username,
                                   password=password,
                                   phone_number=phone_number,
                                   user_role=UserRole.CUSTOMER,
                                   birth_day=birth_day,
                                   address=address,
                                   sex=sex
                                   )
                return redirect('/customer/login')
            else:
                err_msg = 'MAT KHAU KHONG KHOP !!!'
        except Exception as ex:
            err_msg = "He thong dang co loi: " + str(ex)
    return render_template('customer/register.html', err_msg=err_msg)


@app.route("/admin_stats/book")
def book_manager():
    return render_template('template_admin/book.html')


@app.route('/admin_stats/logout')
def admin_logout():
    logout_user()
    return redirect(url_for('admin_login'))


@app.route('/employee/logout')
def employee_logout():
    logout_user()
    return redirect(url_for('employee_login'))


@app.route('/customer/logout')
def customer_logout():
    logout_user()
    return redirect(url_for('customer_login'))


@app.route('/employee')
def employee():
    return render_template('layout/base_employee.html')


@app.route('/employee/login', methods=['get', 'post'])
def employee_login():
    err_msg = ""
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        user_role = request.form.get('user_role')
        u = utils.auth_employee(username=username, password=password, role=UserRole.EMPLOYEE)
        if u:
            login_user(u)
            return redirect('/employee')
        else:
            err_msg = "Tai khoan hoac mat khau sai !!!"
    return render_template('employee/login.html', err_msg=err_msg)


@app.route('/customer/login', methods=['get', 'post'])
def customer_login():
    err_msg = ""
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        user_role = request.form.get('user_role')
        u = utils.auth_user(username=username, password=password, role=UserRole.CUSTOMER)
        if u:
            login_user(u)
            return redirect('/')
        else:
            err_msg = "Tai khoan hoac mat khau sai !!!"
    return render_template('customer/login.html', err_msg=err_msg)


@app.route('/employee/trangchu')
def employee_trangchu():
    return render_template('employee/trangchu.html')


@app.route('/employee/scanner')
def scanner():
    return render_template('employee/scanner.html')


@app.route('/employee/sell_book')
def sell():
    return render_template('employee/sell_book.html')


@app.route('/api/get_book', methods=['GET'])
def get_book():
    code = request.args.get('code')  # Lấy mã sách từ query string
    book = Book.query.filter_by(code=code).first()

    if book:
        # Trả về thông tin sách dưới dạng JSON
        return jsonify({
            'id': book.id,
            'name': book.name,
            'author_id': book.author_id,
            'year_model': book.year_model,
            'unit_price': book.unit_price,
            'code': book.code,
            'units_in_stock': book.units_in_stock,
            'category_id': book.category_id
        })
    else:
        return jsonify({'error': 'Không tìm thấy sách với mã này'}), 404


@app.route('/api/create_offline_order', methods=[('get'), ('post')])
def create_offline_order():
    code = request.args.get('code')  # Lấy mã sách từ query string
    book = Book.query.filter_by(code=code).first()
    quantity_order = request.args.get('quantity')

    if book:
        order = Order(order_date=datetime.now(), payment_id='payment_id', type_order=TypeOrder.OFFLINE_ORDER,
                      employee_id=current_user.get_id())
        if (Book.units_in_stock > 0 and Book.units_in_stock < quantity_order):
            db.session.add(order)
            Book.units_in_stock = Book.units_in_stock - quantity_order
            db.session.commit()


@app.context_processor
def common_processor():
    return {
        'categories': utils.load_categories(),
        'cart_stats': utils.stats_cart(session.get('cart'))
    }


if __name__ == "__main__":
    from app.admin import *

    app.run(debug=True)
