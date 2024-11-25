from tkinter import PhotoImage

from flask_sqlalchemy.model import Model
from jinja2.debug import fake_traceback
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.testing import fails

from app import db, app
from enum import Enum as RoleEnum
from flask_login import UserMixin
import hashlib


class UserRole(RoleEnum):
    ADMIN = 1
    CUSTOMER = 2
    EMPLOYEE = 3


class PhoneNumber(db.Model):
    PhoneNumber = Column(String(12), primary_key=True, nullable=False)
    Type = Column(String(50), nullable=False, default=0)
    Users = relationship('User', backref='phone_number', lazy=True)


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(255),
                    default="")
    user_role = Column(Enum(UserRole), default=UserRole.CUSTOMER)
    Birth_day = Column(DateTime, nullable=False)
    Sex = Column(String(50), nullable=False)
    Address = Column(String(255), nullable=False)
    PhoneNumber_id = Column(String(12), ForeignKey(PhoneNumber.PhoneNumber), nullable=False, default=0)
    Order = relationship('Order', backref='User', lazy=True, foreign_keys='Order.Customer_id')


class Category(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(50), nullable=False)
    Books = relationship('Book', backref='Category', lazy=True)


class Author(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(50), nullable=False)
    Books = relationship('Book', backref='Author', lazy=True)


class Book(db.Model):
    id = Column(String(10), primary_key=True)
    Name = Column(String(100), nullable=False)
    Author_id = Column(Integer, ForeignKey(Author.id), nullable=False)
    Year_model = Column(Integer)
    UnitPrice = Column(Float, nullable=False)
    Code = Column(String(255), nullable=False)
    image = Column(String(100), nullable=True,
                   default="")
    UnitsInStock = Column(Integer, nullable=False)
    Category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    OrderDetails = relationship('OrderDetail', backref='Book', lazy=True)


class Payment(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(50), nullable=False)
    Orders = relationship('Order', backref='payment', lazy=True)


class Order(db.Model):
    id = Column(String(10), primary_key=True)
    TotalPrice = Column(Float, nullable=False, default=0)
    OrderDate = Column(DateTime, nullable=False)
    Payment_id = Column(Integer, ForeignKey(Payment.id), nullable=False)
    OrderDetails = relationship('OrderDetail', backref='Order', lazy=True)
    Customer_id = Column(Integer, ForeignKey(User.id), nullable=False)
    Employee_id = Column(Integer, ForeignKey(User.id), nullable=False)
    user = relationship("User", back_populates="Order", foreign_keys=[Customer_id])  # Chỉ định cột user_id


class OrderDetail(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    Book_id = Column(String(10), ForeignKey(Book.id), nullable=False)
    Order_id = Column(String(10), ForeignKey(Order.id), nullable=False)
    Quantity = Column(Integer, nullable=False, default=1)
    UnitPrice = Column(Integer, nullable=False, default=0)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # categorys = [{
        #     'Name': 'Văn Hóa'
        # }, {
        #     'Name': 'Du Lịch'
        # }, {
        #     'Name': 'Tâm Lý'
        # }, {
        #     'Name': 'Giáo Dục'
        # }, {
        #     'Name': 'Tâm Linh'
        # }, {
        #     'Name': 'Tôn Giáo'
        # }, {
        #     'Name': 'Đời Sống'
        # }, {
        #     'Name': 'Sách Chuyên Ngành'
        # }, {
        #     'Name': 'Tạp Chí'
        # }, {
        #     'Name': 'Sách Học Ngoại Ngữ'
        # }, {
        #     'Name': 'Truyện Tranh'
        # }, {
        #     'Name': 'Tuổi Mới Lớn'
        # }, {
        #     'Name': 'Thiếu Nhi'
        # }, {
        #     'Name': 'Văn Học'
        # }]
        # for c in categorys:
        #     cate = Category(**c)
        #     db.session.add(cate)
        # db.session.commit()
        # authors = [{
        #     'Name' : 'Thích Nhất Hạnh'
        # }, {
        #     'Name' : 'Phạm Công Luận'
        # }, {
        #     'Name' : 'Tô Hoài'
        # }, {
        #     'Name' : 'Nguyễn Nhật Ánh'
        # }, {
        #     'Name' : 'Nguyễn Ngọc Tư'
        # }, {
        #     'Name' : 'Đỗ Hồng Ngọc'
        # }, {
        #     'Name' : 'Dương Thụy'
        # }, {
        #     'Name' : 'Anh Khang'
        # }, {
        #     'Name' : 'Keigo Higashino'
        # }, {
        #     'Name' : 'Dale Carnegie'
        # }]
        # for a in authors:
        #     author = Author(**a)
        #     db.session.add(author)
        # db.session.commit()
        books = [{
            'id': '0000000001',
            'Name': 'Nghệ Thuật Thiết Lập Truyền Thông',
            'Author_id': 1,
            'Year_model' : 2024,
            'UnitPrice' : 105000,
            'Code' : '893200013511',
            'image' : '',
            'UnitsInStock' : 10,
            'Category_id' : 7
        }, {
            'id': '0000000002',
            'Name': 'Giới Bản Khất Sĩ Tân Tu - Nghi Thức Tụng Giới Nữ Khất Sĩ (Tái bản năm 2024)',
            'Author_id': 1,
            'Year_model' : 2024,
            'UnitPrice' : 125000,
            'Code' : '893200013504',
            'image' : '',
            'UnitsInStock' : 10,
            'Category_id' : 3
        }, {
            'id': '0000000003',
            'Name': 'Truyện Tranh Khoa Học Về Các Loài Côn Trùng - Lính Trinh Sát Dũng Cảm - Kiến Polyergus',
            'Author_id': 11,
            'Year_model' : 2024,
            'UnitPrice' : 58000,
            'Code' : '893521237025',
            'image' : '',
            'UnitsInStock' : 10,
            'Category_id' : 13
        }, {
            'id': '0000000004',
            'Name': 'Truyện Tranh Khoa Học Về Các Loài Côn Trùng - Lính Trinh Sát Dũng Cảm - Kiến Polyergusg',
            'Author_id': 1,
            'Year_model' : 2024,
            'UnitPrice' : 105000,
            'Code' : '893200013511',
            'image' : '',
            'UnitsInStock' : 10,
            'Category_id' : 7
        }, {
            'id': '0000000005',
            'Name': 'Kĩ Năng Ứng Xử Cho Bé - Ở Trường Mẫu Giáo',
            'Author_id': 10,
            'Year_model' : 2024,
            'UnitPrice' : 80000,
            'Code' : '893521031038',
            'image' : '',
            'UnitsInStock' : 10,
            'Category_id' : 13
        }, {
            'id': '0000000006',
            'Name': 'Ninja Rantaro - Tập 41',
            'Author_id': 12,
            'Year_model' : 2024,
            'UnitPrice' : 40000,
            'Code' : '893535261927',
            'image' : '',
            'UnitsInStock' : 10,
            'Category_id' : 11
        }, {
            'id': '0000000007',
            'Name': 'Vườn Thú Omagadoki - Tập 3',
            'Author_id': 12,
            'Year_model' : 2024,
            'UnitPrice' : 35000,
            'Code' : '893535261829',
            'image' : '',
            'UnitsInStock' : 10,
            'Category_id' : 11
        }, {
            'id': '0000000008',
            'Name': 'Làng Làng Phố Phố Hà Nội',
            'Author_id': 5,
            'Year_model' : 2024,
            'UnitPrice' : 180000,
            'Code' : '893523524253',
            'image' : '',
            'UnitsInStock' : 10,
            'Category_id' : 14
        }, {
            'id': '0000000009',
            'Name': 'Chuyện Cơm Hội An - Thức Ăn Và Cộng Đồng Ở Một Đô Thị Việt Nam',
            'Author_id': '3',
            'Year_model' : 2024,
            'UnitPrice' : 255000,
            'Code' : '893614420219',
            'image' : '',
            'UnitsInStock' : 10,
            'Category_id' : 2
        }
        ]
        for b in books:
            book = Book(**b)
            db.session.add(book)
        db.session.commit()
