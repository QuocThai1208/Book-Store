from app import db
from sqlalchemy import func
from app.models import Category, Book, Author, OrderDetail, Order, User
from sqlalchemy.sql import extract
import hashlib


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



#Tính tổng doanh thu theo tháng
def month_revenue_total(month):
    return db.session.query(extract('month', Order.order_date),
                            func.sum(OrderDetail.quantity * OrderDetail.unit_price)
                            ).join(OrderDetail, OrderDetail.order_id.__eq__(Order.id)
                            ).filter(extract('month', Order.order_date) == month
                            ).group_by(extract('month', Order.order_date)
                            ).all()

#Tính tổng doanh thu theo năm
def year_revenue_total(year):
    return db.session.query(extract('year', Order.order_date),
                            func.sum(OrderDetail.quantity * OrderDetail.unit_price)
                            ).join(OrderDetail, OrderDetail.order_id.__eq__(Order.id)
                            ).filter(extract('year', Order.order_date) == year
                            ).group_by(extract('year', Order.order_date)
                            ).all()

def add_user(name,username,password, **kwargs):
    user= User(name=name,
               username=username,
               password=str(hashlib.md5(password.strip().encode('utf-8')).hexdigest()),
               avatar= kwargs.get('avatar')
               )
    db.session.add(user)
    db.session.commit()

def auth_user(username, password):
    password = hashlib.md5(password.strip().encode('utf-8')).hexdigest()
    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()

def get_user_by_id(id):
    return User.query.get(id)


