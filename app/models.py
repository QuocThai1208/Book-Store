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
    PhoneNumber = Column(String(12),primary_key=True, nullable=False)
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
    Order = relationship('Order', backref='User', lazy=True)

class Category(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(50), nullable=False)
    Books = relationship('Book', backref='Category', lazy=True)


class Book(db.Model):
    id = Column(String(10), primary_key=True)
    Name = Column(String(100), nullable=False)
    Author = Column(String(50), nullable=False)
    Year_model = Column(Integer)
    UnitPrice = Column(Float, nullable=False)
    Code = Column(String(255), nullable=False)
    image = Column(String(100), nullable=True,
                   default="")
    UnitsInStock = Column(Integer, nullable=False)
    Category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    OrderDetails = relationship('Book', backref='orderdetail', lazy=True)


class Payment(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(50), nullable=False)
    Orders = relationship('Order', backref='payment', lazy=True)


class Order(db.Model):
    id = Column(String(10), primary_key=True)
    TotalPrice = Column(Float, nullable=False, default=0)
    OrderDate = Column(DateTime, nullable=False)
    Payment_id = Column(Integer, ForeignKey(Payment.id), nullable=False)
    OrderDetails = relationship('order', backref='orderdetail', lazy=True)
    Customer_id = Column(Integer, ForeignKey(User.id), nullable=False)
    Employee_id = Column(Integer, ForeignKey(User.id), nullable=False)

class OrderDetail(db.Model):
    id = Column(Integer, primary_key=True,autoincrement=True)
    Book_id = Column(String(10), ForeignKey(Book.id), nullable=False)
    Order_id = Column(String(10), ForeignKey(Order.id), nullable=False)
    Quantity = Column(Integer, nullable=False, default=1)
    UnitPrice = Column(Integer, nullable=False, default=0)






if __name__ == '__main__':
    with app.app_context():
        db.create_all()
