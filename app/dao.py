

from app import db, app
from app.models import Book, OrderSupplier, OrderSupplierDetail, Image, Order
from flask import jsonify
from datetime import datetime, timedelta

def check_order_overdue():
    now = datetime.now()

    order_overdue = Order.query.filter(Order.is_paid == False,
                                       Order.order_date <= now - timedelta(days=2)).all()

    for order in order_overdue:
        for detail in order.order_details:
            book = detail.book
            if book:
                book.units_in_stock += detail.quantity
        db.session.delete(order)
    db.session.commit()

from app.models import Book, OrderSupplier, OrderSupplierDetail, Image
from flask import jsonify ,request
from datetime import datetime
def add_order_supplier_detail(data, order_supplier_id):
    for d in data:
        book_id = int(d.get('id'))
        quantity = int(d.get('quantity'))
        o = OrderSupplierDetail(order_supplier_id=order_supplier_id,
                                book_id=book_id,
                                quantity=quantity,
                                unit_price=Book.query.get(book_id).unit_price)
        db.session.add(o)
    db.session.commit()


def add_order_supplier(data):
    quantity_total = 0
    unit_price_total = 0
    employee_id = 0
    for d in data:
        book_id = int(d.get('id'))
        quantity_total += int(d.get('quantity'))
        unit_price_total += (Book.query.get(book_id).unit_price * int(d.get('quantity')))
        employee_id = int(d.get('employee_id'))
    order_supplier = OrderSupplier(employee_id=employee_id,
                                   create_date=datetime.now(),
                                   quantity_total=quantity_total,
                                   unit_price_total=unit_price_total)
    db.session.add(order_supplier)

    db.session.commit()
    add_order_supplier_detail(data, order_supplier.id)
    return order_supplier


def update_quantity_book(data):
    for d in data:
        book_id = int(d.get('id'))
        quantity = int(d.get('quantity'))

        book = Book.query.get(book_id)
        if book:
            book.units_in_stock += quantity
        else:
            return jsonify({'error': f'Sách với ID {book_id} không tồn tại!'}), 404
    db.session.commit()

def upload_image(images):
    last_book = db.session.query(Book).order_by(Book.id.desc()).first()#lấy id cuối cùng
    new_book_id = last_book.id+1
    for i in images:
        image = Image(name=i.filename, books=new_book_id)
        db.session.add(image)
    db.session.commit()

