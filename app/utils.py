from app import db
from sqlalchemy import func
from app.models import Category, Book, Author, OrderDetail, Order


# thống kê số lượng của từng loại sách
def category_stats():
    return db.session.query(Category.id, Category.name, func.count(Book.id)).join(Book, Category.id.__eq__(
        Book.category_id), isouter=True).group_by(Category.id, Category.name).all()


# Thống kê theo danh thu của sách
def book_stats(kw=None, from_date=None, to_date=None, author=None, category=None):
    b = db.session.query(Book.id, Book.name, func.sum(OrderDetail.quantity * OrderDetail.unit_price)).join(
        OrderDetail, OrderDetail.book_id.__eq__(Book.id), isouter=True).join(Order, Order.id.__eq__(
        OrderDetail.order_id), isouter=True).join(Author, Author.id.__eq__(Book.author_id)).join(Category,Category.id.__eq__(  Book.category_id)).group_by( Book.id, Book.name)

    if kw:
        b = b.filter(Book.name.contains(kw))
    if from_date:
        b = b.filter(Order.order_date.__ge__(from_date))  # so sánh lớn hơn
    if to_date:
        b = b.filter(Order.order_date.__le__(to_date))  # so sánh nhỏ hơn
    if author:
        b = b.filter(Author.name.contains(author))
    if category:
        b = b.filter(Category.name.contains(category))
    return b.all()

#Thống kê số lượng tồn kho
def inventory_stats(name=None):
        b = db.session.query(Book.id, Book.name, Book.units_in_stock)
        if name:
            b = b.filter(Book.name.contains(name))
        return b.all()
