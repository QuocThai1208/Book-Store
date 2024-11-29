from app import db
from sqlalchemy import func
from app.models import Category, Book, Author, OrderDetail, Order


# thống kê số lượng của từng loại sách
def category_stats():
    return db.session.query(Category.id, Category.Name, func.count(Book.id)).join(Book, Category.id.__eq__(
        Book.Category_id), isouter=True).group_by(Category.id, Category.Name).all()


# Thống kê theo danh thu của sách
def book_stats(kw=None, from_date=None, to_date=None, author=None, category=None):
    b = db.session.query(Book.id, Book.Name, func.sum(OrderDetail.Quantity * OrderDetail.UnitPrice)).join(
        OrderDetail, OrderDetail.Book_id.__eq__(Book.id), isouter=True).join(Order, Order.id.__eq__(
        OrderDetail.Order_id), isouter=True).join(Author, Author.id.__eq__(Book.Author_id)).join(Category,Category.id.__eq__(  Book.Category_id)).group_by( Book.id, Book.Name)

    if kw:
        b = b.filter(Book.Name.contains(kw))
    if from_date:
        b = b.filter(Order.OrderDate.__ge__(from_date))  # so sánh lớn hơn
    if to_date:
        b = b.filter(Order.OrderDate.__le__(to_date))  # so sánh nhỏ hơn
    if author:
        b = b.filter(Author.Name.contains(author))
    if category:
        b = b.filter(Category.Name.contains(category))
    return b.all()

#Thống kê số lượng tồn kho
def inventory_stats(name=None):
        b = db.session.query(Book.id, Book.Name, Book.UnitsInStock)
        if name:
            b = b.filter(Book.Name.contains(name))
        return b.all()
