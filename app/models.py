from tkinter import PhotoImage

from flask_sqlalchemy.model import Model
from jinja2.debug import fake_traceback
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.testing import fails

from app import db, app
from enum import Enum as RoleEnum
from enum import Enum as OrderEnum
from flask_login import UserMixin
import hashlib


class UserRole(RoleEnum):
    ADMIN = 1
    CUSTOMER = 2
    EMPLOYEE = 3


class TypeOrder(OrderEnum):
    ONLINE_ORDER = 1
    OFFLINE_ORDER = 2


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(255),
                    default="")
    user_role = Column(Enum(UserRole), default=UserRole.CUSTOMER)
    birth_day = Column(DateTime, nullable=False)
    sex = Column(String(50), nullable=False)
    address = Column(String(255), nullable=False)
    phone_number = relationship('PhoneNumber', backref='User', lazy=True)
    Order = relationship('Order', backref='User', lazy=True, foreign_keys='Order.customer_id')


class PhoneNumber(db.Model):
    phone_number = Column(String(12), primary_key=True, nullable=False)
    type = Column(String(50), nullable=False, default=0)
    users = Column(Integer, ForeignKey(User.id), nullable=False)

    def __str__(self):
        return self.phone_number


class Category(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    books = relationship('Book', backref='Category', lazy=True)

    def __str__(self):
        return self.name



class Author(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    books = relationship('Book', backref='Author', lazy=True)

    def __str__(self):
        return self.name


class Book(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    author_id = Column(Integer, ForeignKey(Author.id), nullable=False)
    year_model = Column(Integer)
    unit_price = Column(Float, nullable=False)
    code = Column(String(255), nullable=False)
    units_in_stock = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    order_details = relationship('OrderDetail', backref='Book', lazy=True)
    images = relationship('Image', backref='Book', lazy=True)

    def __str__(self):
        return str(self.name) + '\n'

class Image(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    books = Column(Integer, ForeignKey(Book.id), nullable=False)

    def __str__(self):
        return self.name

class Payment(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    orders = relationship('Order', backref='Payment', lazy=True)


class Order(db.Model):
    id = Column(String(10), primary_key=True)
    order_date = Column(DateTime, nullable=False)
    payment_id = Column(Integer, ForeignKey(Payment.id), nullable=False)
    type_order = Column(Enum(TypeOrder), default=TypeOrder.ONLINE_ORDER)
    order_details = relationship('OrderDetail', backref='Order', lazy=True)
    customer_id = Column(Integer, ForeignKey(User.id), nullable=False)
    employee_id = Column(Integer, ForeignKey(User.id), nullable=False)
    user = relationship("User", back_populates="Order", foreign_keys=[customer_id])  # Chỉ định cột user_id

    def __str__(self):
        return self.id


class OrderDetail(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey(Book.id), nullable=False)
    order_id = Column(String(10), ForeignKey(Order.id), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Integer, nullable=False, default=0)


if __name__ == '__main__':
    with app.app_context():
        # db.create_all()
        # categorys = [{
        #     'name': 'Văn Hóa'
        # }, {
        #     'name': 'Du Lịch'
        # }, {
        #     'name': 'Tâm Lý'
        # }, {
        #     'name': 'Giáo Dục'
        # }, {
        #     'name': 'Tâm Linh'
        # }, {
        #     'name': 'Tôn Giáo'
        # }, {
        #     'name': 'Đời Sống'
        # }, {
        #     'name': 'Sách Chuyên Ngành'
        # }, {
        #     'name': 'Tạp Chí'
        # }, {
        #     'name': 'Sách Học Ngoại Ngữ'
        # }, {
        #     'name': 'Truyện Tranh'
        # }, {
        #     'name': 'Tuổi Mới Lớn'
        # }, {
        #     'name': 'Thiếu Nhi'
        # }, {
        #     'name': 'Văn Học'
        # }]
        # for c in categorys:
        #     cate = Category(**c)
        #     db.session.add(cate)
        # db.session.commit()
        # authors = [{
        #     'name' : 'Thích Nhất Hạnh'
        # }, {
        #     'name' : 'Phạm Công Luận'
        # }, {
        #     'name' : 'Tô Hoài'
        # }, {
        #     'name' : 'Nguyễn Nhật Ánh'
        # }, {
        #     'name' : 'Nguyễn Ngọc Tư'
        # }, {
        #     'name' : 'Đỗ Hồng Ngọc'
        # }, {
        #     'name' : 'Dương Thụy'
        # }, {
        #     'name' : 'Anh Khang'
        # }, {
        #     'name' : 'Keigo Higashino'
        # }, {
        #     'name' : 'Dale Carnegie'
        # }]
        # for a in authors:
        #     author = Author(**a)
        #     db.session.add(author)
        # db.session.commit()
        books = [{
            'name': 'Nghệ Thuật Thiết Lập Truyền Thông',
            'author_id': 1,
            'year_model' : 2024,
            'unit_price' : 105000,
            'code' : '893200013511',
            'units_in_stock' : 10,
            'category_id' : 7
        }, {
            'name': 'Giới Bản Khất Sĩ Tân Tu - Nghi Thức Tụng Giới Nữ Khất Sĩ (Tái bản năm 2024)',
            'author_id': 1,
            'year_model' : 2024,
            'unit_price' : 125000,
            'code' : '893200013504',
            'units_in_stock' : 10,
            'category_id' : 3
        }, {
            'name': 'Truyện Tranh Khoa Học Về Các Loài Côn Trùng - Lính Trinh Sát Dũng Cảm - Kiến Polyergus',
            'author_id': 10,
            'year_model' : 2024,
            'unit_price' : 58000,
            'code' : '893521237025',
            'units_in_stock' : 10,
            'category_id' : 13
        }, {
            'name': 'Truyện Tranh Khoa Học Về Các Loài Côn Trùng - Lính Trinh Sát Dũng Cảm - Kiến Polyergusg',
            'author_id': 1,
            'year_model' : 2024,
            'unit_price' : 105000,
            'code' : '893200013511',
            'units_in_stock' : 10,
            'category_id' : 7
        }, {
            'name': 'Kĩ Năng Ứng Xử Cho Bé - Ở Trường Mẫu Giáo',
            'author_id': 10,
            'year_model' : 2024,
            'unit_price' : 80000,
            'code' : '893521031038',
            'units_in_stock' : 10,
            'category_id' : 13
        }, {
            'name': 'Ninja Rantaro - Tập 41',
            'author_id': 5,
            'year_model' : 2024,
            'unit_price' : 40000,
            'code' : '893535261927',
            'units_in_stock' : 10,
            'category_id' : 11
        }, {
            'name': 'Vườn Thú Omagadoki - Tập 3',
            'author_id': 9,
            'year_model' : 2024,
            'unit_price' : 35000,
            'code' : '893535261829',
            'units_in_stock' : 10,
            'category_id' : 11
        }, {
            'name': 'Làng Làng Phố Phố Hà Nội',
            'author_id': 5,
            'year_model' : 2024,
            'unit_price' : 180000,
            'code' : '893523524253',
            'units_in_stock' : 10,
            'category_id' : 14
        }, {
            'name': 'Chuyện Cơm Hội An - Thức Ăn Và Cộng Đồng Ở Một Đô Thị Việt Nam',
            'author_id': 3,
            'year_model' : 2024,
            'unit_price' : 255000,
            'code' : '893614420219',
            'units_in_stock' : 10,
            'category_id' : 2
        }
        ]
        for b in books:
            book = Book(**b)
            db.session.add(book)
        db.session.commit()
