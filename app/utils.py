from app import db
from sqlalchemy import func
from app.models import Category, Book, Author


# thống kê số lượng của từng loại sách
def category_stats():
    return db.session.query(Category.id, Category.Name, func.count(Book.id)).join(Book, Category.id.__eq__(
        Book.Category_id), isouter=True).group_by(Category.id, Category.Name).all()
