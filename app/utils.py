import datetime
import hashlib

from flask_login import current_user
from sqlalchemy import func
from sqlalchemy.sql import extract

from app import app, db
from app.models import Category, Book, Author, OrderDetail, Order, User, UserRole, Image, TypeOrder
from datetime import datetime, timedelta

def get_order_overdue(customer_id):
    now = datetime.now()
    return Order.query.filter(Order.customer_id==customer_id, Order.is_paid==False).all()

# thống kê số lượng của từng loại sách
def category_stats():
    return db.session.query(Category.id, Category.name, func.count(Book.id)).join(Book, Category.id.__eq__(
        Book.category_id), isouter=True).group_by(Category.id, Category.name).all()


# Thống kê số lượng tồn kho
def inventory_stats(name=None):
    b = db.session.query(Book.id, Book.name, Book.units_in_stock)
    if name:
        b = b.filter(Book.name.contains(name))
    return b.all()


def revenue(type_revenue, month, year):
    if type_revenue == 'revenue-day':
        return db.session.query(extract('day', Order.order_date),
                                func.sum(OrderDetail.quantity * OrderDetail.unit_price)
                                ).join(OrderDetail, OrderDetail.order_id.__eq__(Order.id), isouter=True
                                       ).filter(extract('month', Order.order_date) == month,
                                                extract('year', Order.order_date) == year
                                                ).group_by(extract('day', Order.order_date)
                                                           ).order_by(extract('day', Order.order_date)).all()

    elif type_revenue == 'revenue-month':
        return db.session.query(extract('month', Order.order_date),
                                func.sum(OrderDetail.quantity * OrderDetail.unit_price)
                                ).join(OrderDetail, OrderDetail.order_id.__eq__(Order.id), isouter=True
                                       ).filter(extract('year', Order.order_date) == year
                                                ).group_by(extract('month', Order.order_date)
                                                           ).order_by(extract('month', Order.order_date)).all()


def revenue_book(from_date=None, to_date=None):
    b = db.session.query(
        Book.id,
        Book.name,
        Category.name,
        func.sum(OrderDetail.quantity * OrderDetail.unit_price)
    ).join(
        OrderDetail, OrderDetail.book_id.__eq__(Book.id), isouter=True
    ).join(Order, Order.id.__eq__(
        OrderDetail.order_id), isouter=True
           ).join(
        Author, Author.id.__eq__(Book.author_id)
    ).join(
        Category, Category.id.__eq__(Book.category_id)
    ).group_by(Book.id, Book.name, Category.name)

    if from_date:
        b = b.filter(Order.order_date.__ge__(from_date))
    if to_date:
        b = b.filter(Order.order_date.__le__(to_date))
    return b.all()

def get_employee():
    return db.session.query(User.name, User.birth_day, User.sex, User.address).filter(User.user_role=='EMPLOYEE').all()

# Tính tổng doanh thu theo tháng
def month_revenue_total(month):
    return db.session.query(extract('month', Order.order_date),
                            func.sum(OrderDetail.quantity * OrderDetail.unit_price)
                            ).join(OrderDetail, OrderDetail.order_id.__eq__(Order.id)
                                   ).filter(extract('month', Order.order_date) == month
                                            ).group_by(extract('month', Order.order_date)
                                                       ).all()


# Tính tổng doanh thu theo năm
def year_revenue_total(year):
    return db.session.query(extract('year', Order.order_date),
                            func.sum(OrderDetail.quantity * OrderDetail.unit_price)
                            ).join(OrderDetail, OrderDetail.order_id.__eq__(Order.id)
                                   ).filter(extract('year', Order.order_date) == year
                                            ).group_by(extract('year', Order.order_date)
                                                       ).all()


def add_user(name, username, password, user_role, birth_day, address, sex, **kwargs):
    user = User(name=name,
                username=username,
                password=str(hashlib.md5(password.strip().encode('utf-8')).hexdigest()),
                avatar=kwargs.get('avatar'),
                user_role=UserRole.EMPLOYEE,
                birth_day=birth_day,
                address=address,
                sex=sex

                )
    db.session.add(user)
    db.session.commit()


def add_customer(name, username, password, user_role, birth_day, address, sex, **kwargs):
    user = User(name=name,
                username=username,
                password=str(hashlib.md5(password.strip().encode('utf-8')).hexdigest()),
                avatar=kwargs.get('avatar'),
                user_role=UserRole.CUSTOMER,
                birth_day=birth_day,
                address=address,
                sex=sex

                )
    db.session.add(user)
    db.session.commit()


def auth_user(username, password, role=UserRole.CUSTOMER):
    password = hashlib.md5(password.strip().encode('utf-8')).hexdigest()
    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password),
                             User.user_role.__eq__(role)).first()


def auth_employee(username, password, role=UserRole.EMPLOYEE):
    password = hashlib.md5(password.strip().encode('utf-8')).hexdigest()
    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password),
                             User.user_role.__eq__(role)).first()


def get_user_by_id(id):
    return User.query.get(id)


def load_categories():
    return Category.query.all()

def get_book_import():
    return db.session.query(Book.id, Book.name, Book.units_in_stock).filter(Book.units_in_stock <= 150).all()




def load_books(cate_id=None, kw=None, page=1):
    query = Book.query

    if kw:
        query = query.filter(Book.name.contains(kw))

    if cate_id:
        query = query.filter(Book.category_id == cate_id)

    page_size = app.config['PAGE_SIZE']
    start = (page - 1) * page_size
    query = query.slice(start, start + page_size)

    return query.all()


def load_book_by_code(code=None):
    return Book.query.filter(Book.code == code).all()

def count_books(cate_id=None, kw=None):
    query = Book.query

    if kw:
        query = query.filter(Book.name.contains(kw))

    if cate_id:
        query = query.filter(Book.category_id == cate_id)

    return query.count()


def get_book_by_id(book_id):
    return Book.query.get(book_id)


def load_img_book(book_id):
    imgs = Image.query.filter(Image.books == book_id)

    return imgs.all()


def get_adv_img():
    return Image.query.limit(7).all()

def stats_cart(cart):
    total_amount, total_quantity = 0, 0

    if cart:
        for c in cart.values():
            total_quantity += c['quantity']
            total_amount += c['quantity'] * c['price']

    return {
        'total_amount': total_amount,
        'total_quantity': total_quantity
    }


def add_receipt(cart):
    if cart:
        user = current_user
        r = Order(customer_id=user.id, employee_id=None, type_order=TypeOrder.ONLINE_ORDER)
        db.session.add(r)

        for c in cart.values():
            d = OrderDetail(quantity=c['quantity'], unit_price=c['price'],
                            Order=r, product_id=c['id'])
            db.session.add(d)

        db.session.commit()


def add_order_in_book_detail(book_id, quantity, unit_price):
    o = Order(User=current_user, order_date=datetime.datetime.now(),
              type_order=TypeOrder.ONLINE_ORDER)
    db.session.add(o)
    d = OrderDetail(quantity=quantity, unit_price=unit_price, book_id=book_id, customer_id=2)
    db.session.add(d)
    db.session.commit()

def search_book_by_code(kw=None):
    query=Book.query
    if kw:
        query=query.filter(Book.code.contains(kw))

    return query.all()

def stats_bill(bill):
    total_amount, total_quantity = 0, 0

    if bill:
        for b in bill.values():
            total_quantity += b['quantity']
            total_amount += b['quantity'] * b['price']

    return {
        'total_amount': total_amount,
        'total_quantity': total_quantity
    }


def get_order_by_id(order_id):
    return Order.query.filter(Order.id == order_id).first()


def get_order_of_customer(customer_id):
    return Order.query.filter(customer_id == customer_id, Order.is_paid == False).all()

