from app import db, app
from app.models import Book, OrderSupplier, OrderSupplierDetail, Image
from flask import jsonify
from datetime import datetime
import requests
import uuid
import hmac
import hashlib

def generate_signature(payload, secret_key):
    raw_data = f"accessKey={payload['accessKey']}&amount={payload['amount']}&extraData={payload['extraData']}&ipnUrl={payload['ipnUrl']}&orderId={payload['orderId']}&orderInfo={payload['orderInfo']}&partnerCode={payload['partnerCode']}&redirectUrl={payload['redirectUrl']}&requestId={payload['requestId']}&requestType={payload['requestType']}"
    signature = hmac.new(secret_key.encode(), raw_data.encode(), hashlib.sha256).hexdigest()
    return signature


def generate_momo_qr(order):
    momo_endpoint = "https://test-payment.momo.vn/v2/gateway/api/create"
    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "partnerCode": "YOUR_PARTNER_CODE",
        "accessKey": "YOUR_ACCESS_KEY",
        "requestId": str(uuid.uuid4()),  # UUID duy nhất cho mỗi yêu cầu
        "amount": order.calculate_total(),  # Tổng số tiền thanh toán
        "orderId": order.id,  # ID đơn hàng
        "orderInfo": f"Payment for order {order.id}",  # Mô tả đơn hàng
        "redirectUrl": "http://yourwebsite.com/orders",  # URL chuyển hướng sau khi thanh toán
        "ipnUrl": "http://yourwebsite.com/ipn",  # URL nhận thông báo từ MoMo
        "extraData": "",  # Dữ liệu bổ sung (có thể để trống)
        "requestType": "captureWallet",  # Loại yêu cầu (cố định là captureWallet)
        "signature": "GENERATED_SIGNATURE"  # Chữ ký để xác thực
    }
    response = requests.post(momo_endpoint, json=payload, headers=headers)
    response_data = response.json()

    if response_data.get("resultCode") == 0:
        return response_data.get("qrCodeUrl")  # URL QR Code
    else:
        raise Exception(f"Failed to generate QR: {response_data.get('message')}")


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

