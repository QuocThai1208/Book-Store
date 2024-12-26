import pdb
import uuid
from calendar import month
from datetime import datetime
from flask import render_template, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql.functions import random

from app import app
import math
from flask import render_template, request, jsonify, url_for, redirect, Response, session
from sqlalchemy.ext.orderinglist import ordering_list

from flask import render_template, request, jsonify, url_for, redirect
from app import app, dao
from app import app, login
from app.models import UserRole, Book, Order, TypeOrder, OrderDetail
from app.utils import revenue
import cv2
from flask import render_template, jsonify, url_for, redirect, flash, request
from flask_login import login_user, logout_user, current_user, login_required

from flask_login import login_user, logout_user
from pyzbar.pyzbar import decode

from app import app, login
from app.models import UserRole, TypeOrder, Order, OrderDetail


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

    return render_template('list_books/book_detail.html', book=book, image=image)

@app.route("/buy_now/<int:book_id>", methods=["POST"])
def buy_now(book_id):
    quantity = request.json.get('quantity', 1)
    book = utils.get_book_by_id(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    if quantity > book.units_in_stock:
        return jsonify({"error": "Not enough stock available"}), 400

    # Tạo Order
    order_id = uuid.uuid4().hex[:10]
    order = Order(
        id=order_id,
        order_date=datetime.now(),
        payment_id=1,
        type_order=TypeOrder.ONLINE_ORDER,
        customer_id=current_user.id,
        employee_id=2,
        guest_name=current_user.name,
        is_paid=False,
    )

    # Tạo OrderDetail
    order_detail = OrderDetail(
        book_id=book_id,
        order_id=order_id,
        quantity=quantity,
        unit_price=book.unit_price
    )

    book.units_in_stock -= quantity

    # Lưu vào database
    try:
        db.session.add(order)
        db.session.add(order_detail)
        db.session.commit()
        return jsonify({"message": "Order created successfully", "order_id": order_id})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to create order", "details": str(e)}), 500


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
            'quantity': 1
        }

    session['cart'] = cart

    return jsonify(utils.stats_cart(cart))


@app.route('/api/cart-with-quantity', methods=['post'])
def add_in_detail():
    cart = session.get('cart')
    if not cart:
        cart = {}

    id = str(request.json.get('id'))
    name = request.json.get('name')
    price = request.json.get('price')
    img = str(request.json.get('img'))
    quantity = request.json.get('quantity')

    if id in cart:
        cart[id]["quantity"] += quantity
    else:
        cart[id] = {
            "id": id,
            "name": name,
            "price": price,
            'img': img,
            'quantity': quantity
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


@app.route('/cre-order', methods=['post'])
def pay():
    cart = session.get('cart')
    user = current_user
    id = str(uuid.uuid4())[:10]
    try:
        o = Order(id=id,
                  order_date=datetime.now(),
                  payment_id=1,
                  type_order=TypeOrder.ONLINE_ORDER,
                  customer_id=user.id,
                  employee_id=2,
                  guest_name=user.name,
                  is_paid=False)
        db.session.add(o)
        db.session.commit()

        for c in cart.values():
            d = OrderDetail(book_id=c['id'], order_id=id, quantity=c['quantity'], unit_price=c['price'])
            book = utils.get_book_by_id(c['id'])
            if c['quantity'] > book.units_in_stock:
                return jsonify({"error": "Không đủ số lượng"}), 400
            else:
                book.units_in_stock -= c['quantity']
            db.session.add(d)

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to create order", "details": str(e)}), 500
    else:
        del session['cart']
        return jsonify({'status': 200, 'order_id': id})

@app.route('/cart')
def cart():
    return render_template('customer/cart.html')

@app.route('/payment/<order_id>')
def pay_order(order_id):
    order = utils.get_order_by_id(order_id)  # Lấy thông tin đơn hàng
    if not order:
        return "Order not found", 404
    #
    # # Tạo thông tin thanh toán MoMo (giả định đã có SDK hoặc tích hợp API MoMo)
    # qr_code_url = dao.generate_momo_qr(order)  # Hàm này trả về URL QR MoMo

    return render_template('customer/pay.html', order=order)

@app.route('/payment')
def list_payment():
    payments=utils.get_order_of_customer(current_user.id)

    return render_template('customer/pays.html', payments=payments)


@app.route('/confirm_payment/<order_id>', methods=['POST'])
@login_required
def confirm_payment(order_id):
    try:
        # Tìm đơn hàng theo ID và đảm bảo thuộc về current_user
        order = Order.query.filter_by(id=order_id, customer_id=current_user.id).first()

        payment_id = request.form.get('payment_id')

        if not order:
            flash("Không tìm thấy đơn hàng hoặc bạn không có quyền truy cập.", "danger")
            return redirect(url_for('list_payment'))  # Điều hướng về danh sách đơn chưa thanh toán

        # Cập nhật trạng thái is_paid = True
        order.is_paid = True
        order.payment_id = payment_id
        db.session.commit()

        flash("Thanh toán thành công. Đơn hàng của bạn đã được cập nhật.", "success")
        return redirect(url_for('list_payment', order_id=order_id))  # Điều hướng đến trang chi tiết đơn hàng
    except SQLAlchemyError as e:
        db.session.rollback()
        flash("Đã xảy ra lỗi trong quá trình xử lý. Vui lòng thử lại.", "danger")
        return redirect(url_for('list_payment'))

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

@app.route("/admin_stats/table-list-employee")
def get_employee():
    return render_template('template_admin/table-list-employee.html', employees=utils.get_employee())


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
    code=request.args.get('code')
    book=utils.search_book_by_code(kw=code)
    return render_template('employee/sell_book.html',book=book,code=code)


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


@app.route('/api/add-bill', methods=['post'])
def add_to_bill():
    bill = session.get('bill')

    if not bill:
        bill={}

    id= str(request.json.get('id'))
    name=request.json.get('name')
    price= request.json.get('price')

    if id in bill:
        bill[id]["quantity"]+=1
    else:
        bill[id]= {
            "id":id,
            "name":name,
            "price":price,
            "quantity":1
            }

    session['bill']= bill

    return jsonify(utils.stats_bill(bill))

@app.route('/api/update-bill', methods=['put', 'delete'])
def update_bill():
    id = str(request.json.get('id'))
    quantity = request.json.get('quantity')

    bill = session.get('bill')

    if bill and id in bill:
        if int(quantity) == 0:
            del bill[id]
        else:
            bill[id]["quantity"] = int(quantity)

        session['bill'] = bill

    return jsonify(utils.stats_bill(bill))

@app.context_processor
def common_processor():
    return {
        'bill_stats': utils.stats_bill(session.get('bill')),
        'categories': utils.load_categories(),
        'cart_stats': utils.stats_cart(session.get('cart'))
    }

@app.route('/api/delete-bill/<book_id>', methods=['delete'])
def delete_bill(book_id):
    bill = session.get('bill')

    if bill and book_id in bill:
        del bill[book_id]
        session['bill'] = bill

    return jsonify(utils.stats_bill(bill))

@app.route('/employee/bill')
def bill():
    return render_template('employee/bill.html')

@app.route('/employee/check_order')
def check_orders():
    return render_template('employee/check_order.html', orders=utils.get_order_overdue())

@app.route('/click-check', methods=['POST'])
def click_check_order():
    try:
        dao.check_order_overdue()
        return jsonify({'message': 'OK'}), 200
    except:
        return jsonify({'error': 'Không thể xóa đơn hàng quá hạn'}), 404
@app.route('/create-order', methods=['POST'])
def create_order():
    data = request.get_json()
    id_order=str(uuid.uuid4())[:10]
    new_order = Order(
        id=id_order,
        order_date=datetime.now(),
        payment_id=data['payment_id'],
        type_order=TypeOrder.OFFLINE_ORDER,
        employee_id=data['employee_id'],
        guest_name=data['guest_name'],
        is_paid=True
    )
    db.session.add(new_order)
    db.session.commit()

    for detail in data['list_book'].values():
        new_order_detail = OrderDetail(
            book_id=detail['id'],
            order_id=id_order,
            quantity=detail['quantity'],
            unit_price=detail['price']
        )
        book = utils.get_book_by_id(detail['id'])
        if detail['quantity'] > book.units_in_stock:
            return jsonify({"error": "Không đủ số lượng sách"}), 400
        else:
            book.units_in_stock -= detail['quantity']
        db.session.add(new_order_detail)

    db.session.commit()

    return jsonify({'message': 'Đơn hàng đã được tạo thành công', 'order': data}), 200


@app.route('/admin_stats/send-order')
def send_order():
    return render_template('template_admin/send-order.html', books=utils.get_book_import())

@app.route('/api/submit-data', methods=['POST'])
def submit_data():
    data = request.get_json()  # Lấy dữ liệu JSON từ client
    dao.update_quantity_book(data)
    order = dao.add_order_supplier(data)
    return jsonify({
        'status': 200,
        'data': order.to_dto()
    })

@app.route('/api/data_Id_Order', methods=['POST'])
def submit_data_is_order():
    data = request.get_json()
    dao.delete_order_overdue(data)
    return jsonify({
        'status': 200,
        'data': "Xóa thành công"
    })

@app.route('/api/upload-images', methods=['POST'])
def upload_images():
    images = request.files.getlist('image')  # Lấy dữ liệu JSON từ client
    dao.upload_image(images)
    return jsonify({
        'status': 200,
        'data': 'Images uploaded successfully'
    })


if __name__ == "__main__":
    from app.admin import *
    app.run(debug=True)